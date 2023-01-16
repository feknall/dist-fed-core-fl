import base64
import json
import pickle
import time

import numpy as np

import mnist_common
from config import Config
from dto import ModelSecretRequest, ModelMetadata
from flevents.event_processor import EventProcessor
from trainer.fedshare.trainer_gateway_rest_api import TrainerGatewayRestApi
from utils import log_msg

config = Config()
client_datasets = mnist_common.load_train_dataset(config.number_of_clients, permute=True)

highest_range = np.finfo('float16').max
# field_size = np.finfo('float32').max

time_list = []


class TrainerEventProcessor(EventProcessor):
    roundCounter = 0
    clientIndex = None
    gateway_rest_api = None

    def __init__(self, client_index, secrets_per_client, gateway_rest_api: TrainerGatewayRestApi):
        self.clientIndex = client_index
        self.gateway_rest_api = gateway_rest_api
        self.secretsPerClient = secrets_per_client

    def train_one_round(self):
        start_time = time.time()

        x_train, y_train = client_datasets[self.clientIndex][0], client_datasets[self.clientIndex][1]
        model = mnist_common.get_model()

        if self.roundWeight is not None:
            log_msg("Using weights of previous round.")
            model.set_weights(self.roundWeight)

        model.fit(x_train, y_train, epochs=config.epochs, batch_size=config.batch_size, verbose=config.verbose,
                  validation_split=config.validation_split, shuffle=True)

        layer_dict, layer_shape, shares_dict = {}, {}, {}
        data = np.array(model.get_weights())
        no_of_layers = len(data)

        for layer_index in range(no_of_layers):
            layer_dict[layer_index] = data[layer_index]
            layer_shape[layer_index] = data[layer_index].shape

        for layer_index in range(no_of_layers):
            shares_dict[layer_index] = np.zeros(shape=(self.secretsPerClient,) + layer_shape[layer_index],
                                                dtype=np.float32)

            for server_index in range(self.secretsPerClient - 1):
                shares_dict[layer_index][server_index] = \
                    np.random.uniform(low=-highest_range, high=highest_range, size=layer_shape[layer_index]).astype(np.float32)

            share_sum_except_last = np.array(shares_dict[layer_index][:self.secretsPerClient - 1]).sum(axis=0,
                                                                                                       dtype=np.float32)
            x = np.copy(np.array(layer_dict[layer_index], dtype=np.float32))
            diff = np.subtract(x, share_sum_except_last, dtype=np.float32)
            # last_share = np.fmod(diff, field_size, dtype=np.float32)
            shares_dict[layer_index][self.secretsPerClient - 1] = diff

        all_servers = []
        for server_index in range(self.secretsPerClient):
            all_servers.append({})

        for server_index in range(self.secretsPerClient):
            for layer_index in range(len(shares_dict)):
                all_servers[server_index][layer_index] = shares_dict[layer_index][server_index]

        weights1 = base64.b64encode(pickle.dumps(all_servers[0])).decode()
        weights2 = base64.b64encode(pickle.dumps(all_servers[1])).decode()
        dataset_size = client_datasets[self.clientIndex][0].shape[0]
        model_secret = ModelSecretRequest(self.modelId, dataset_size, weights1, weights2)

        self.gateway_rest_api.add_model_secret(model_secret)

        log_msg("Secrets are sent.")

        log_msg(f"Round {self.roundCounter} completed.")

        self.roundCounter = self.roundCounter + 1
        log_msg("Waiting...")
        time_list.append((start_time, time.time() - start_time))

    def start_training_event(self, event_payload):
        x = json.loads(event_payload)
        metadata = ModelMetadata(**x)
        log_msg(f"EVENT: A model training started. modelId: {metadata.modelId}")
        self.modelId = metadata.modelId
        self.train_one_round()

    def round_finished(self, event_payload):
        end_round_model = self.gateway_rest_api.get_end_round_model(self.modelId)
        self.roundWeight = pickle.loads(base64.b64decode(end_round_model.weights))
        self.train_one_round()

    def training_finished(self, event_payload):
        log_msg("Training finiiiiiiiiiiiiiiished :D")
        log_msg(f"trainer_time_list = {time_list}")
        exit()

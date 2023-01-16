import base64
import json
import pickle
import time

import numpy as np

import mnist_common
from config import Config
from dto import OriginalModelRequest, FedAvgModelMetadata
from flevents.event_processor import EventProcessor
from trainer.fedavg.trainer_gateway_rest_api import TrainerGatewayRestApi
from utils import log_msg

config = Config()
client_datasets = mnist_common.load_train_dataset(config.number_of_clients, permute=True)


time_list = []


class TrainerEventProcessor(EventProcessor):
    roundCounter = 0
    clientIndex = None
    gateway_rest_api = None

    def __init__(self, client_index, gateway_rest_api: TrainerGatewayRestApi):
        self.clientIndex = client_index
        self.gateway_rest_api = gateway_rest_api

    def train_one_round(self):
        start_time = time.time()

        x_train, y_train = client_datasets[self.clientIndex][0], client_datasets[self.clientIndex][1]
        model = mnist_common.get_model()

        if self.roundWeight is not None:
            log_msg("Using weights of previous round.")
            model.set_weights(self.roundWeight)

        model.fit(x_train, y_train, epochs=config.epochs, batch_size=config.batch_size, verbose=config.verbose,
                  validation_split=config.validation_split, shuffle=True)

        weight = base64.b64encode(pickle.dumps(np.array(model.get_weights()))).decode()
        dataset_size = client_datasets[self.clientIndex][0].shape[0]

        original_model = OriginalModelRequest(self.modelId, dataset_size, weight)

        self.gateway_rest_api.add_original_model(original_model)

        log_msg("Secrets are sent.")

        log_msg(f"Round {self.roundCounter} completed.")

        self.roundCounter = self.roundCounter + 1
        log_msg("Waiting...")
        time_list.append((start_time, time.time() - start_time))

    def start_training_event(self, event_payload):
        x = json.loads(event_payload)
        metadata = FedAvgModelMetadata(**x)
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

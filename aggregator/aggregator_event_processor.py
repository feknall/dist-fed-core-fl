import base64
import json
import pickle
import time

import numpy as np

from aggregator.aggregator_gateway_rest_api import AggregatorGatewayRestApi
from flevents.event_processor import EventProcessor
from dto import ModelSecretResponse, AggregatedSecret, ModelMetadata
from utils import log_msg

time_list = []


class AggregatorEventProcessor(EventProcessor):
    current_round = -1
    gateway_rest_api = None

    def __init__(self, gateway_rest_api: AggregatorGatewayRestApi):
        self.gateway_rest_api = gateway_rest_api

    def model_secret_added(self, event_payload):
        x = json.loads(event_payload)
        model_secret = ModelSecretResponse(**x)
        log_msg(f"EVENT: A model secret is added. modelId: {model_secret.modelId}")

        if self.current_round >= model_secret.round:
            log_msg("Already started. Ignoring...")
            return

        if not self.gateway_rest_api.check_all_secrets_received(self.modelId):
            log_msg("Waiting for more secrets...")
            return

        start_time = time.time()
        log_msg("Aggregator is started :)")

        self.current_round = model_secret.round

        secrets = self.gateway_rest_api.get_model_secrets_for_current_round(self.modelId)

        clients_secret = []
        dataset_size_list = []
        for secret in secrets:
            clients_secret.append(pickle.loads(base64.b64decode(secret.weights)))
            dataset_size_list.append(secret.datasetSize)
        total_dataset_size = sum(dataset_size_list)

        log_msg(f"Trying to aggregate {len(clients_secret)} secrets")

        model = {}
        for layer_index in range(len(clients_secret[0])):
            alpha_list = []
            for client_index in range(len(clients_secret)):
                alpha = clients_secret[client_index][layer_index] * (
                        dataset_size_list[client_index] / total_dataset_size)
                alpha_list.append(alpha)
            model[layer_index] = np.array(alpha_list).sum(axis=0, dtype=np.float32)

        model_byte = base64.b64encode(pickle.dumps(model)).decode()

        aggregated_secret = AggregatedSecret(self.modelId, model_byte)

        self.gateway_rest_api.add_aggregated_secret(aggregated_secret)

        log_msg("Aggregation finished successfully.")
        time_list.append((start_time, time.time() - start_time))

    def start_training_event(self, event_payload):
        x = json.loads(event_payload)
        metadata = ModelMetadata(**x)
        log_msg(f"EVENT: A model training started. modelId: {metadata.modelId}")
        self.modelId = metadata.modelId

    def training_finished(self, event_payload):
        log_msg("Training finiiiiiiiiiiiiiiished :D")
        log_msg(f"aggregator_time_list = {time_list}")
        exit()
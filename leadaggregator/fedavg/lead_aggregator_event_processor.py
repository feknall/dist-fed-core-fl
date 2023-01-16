import base64
import json
import pickle
import time

import numpy as np

from dto import EndRoundModel, ModelMetadata, OriginalModel, FedAvgModelMetadata, OriginalModelRequest, \
    OriginalModelResponse
from flevents.event_processor import EventProcessor
from leadaggregator.fedavg.lead_aggregator_gateway_rest_api import LeadAggregatorGatewayRestApi
from utils import log_msg

time_list = []


class LeadAggregatorEventProcessor(EventProcessor):
    current_round = -1
    gateway_rest_api = None

    def __init__(self, gateway_rest_api: LeadAggregatorGatewayRestApi):
        self.gateway_rest_api = gateway_rest_api

    def original_model_added_event(self, event_payload):
        x = json.loads(event_payload)
        original_model = OriginalModelResponse(**x)
        log_msg(f"EVENT: A aggregated secret for a model is added. modelId: {original_model.modelId}")

        if self.current_round >= original_model.round:
            log_msg("Already started. Ignoring...")
            return

        if not self.gateway_rest_api.check_all_original_models_received(self.modelId):
            log_msg("Waiting for more aggregated secrets...")
            return
        start_time = time.time()
        log_msg("Lead aggregator is started :)")

        self.current_round = original_model.round

        original_models = self.gateway_rest_api.get_original_models_for_current_round(self.modelId)

        decoded_original_models = []
        dataset_size_list = []
        for original_model in original_models:
            decoded_original_models.append(pickle.loads(base64.b64decode(original_model.weights)))
            dataset_size_list.append(original_model.datasetSize)
        log_msg(f"Trying to aggregate {len(decoded_original_models)} secrets")

        total_dataset_size = sum(dataset_size_list)

        model = {}
        for layer_index in range(len(decoded_original_models[0])):
            alpha_list = []
            for client_index in range(len(decoded_original_models)):
                alpha = decoded_original_models[client_index][layer_index] * (
                        dataset_size_list[client_index] / total_dataset_size)
                alpha_list.append(alpha)
            model[layer_index] = np.array(alpha_list).sum(axis=0, dtype=np.float32)

        model_byte = base64.b64encode(pickle.dumps(model)).decode()

        aggregated_secret = EndRoundModel(self.modelId, model_byte)

        self.gateway_rest_api.add_end_round_model(aggregated_secret)

        log_msg("Aggregation finished successfully.")
        time_list.append((start_time, time.time() - start_time))

    def start_training_event(self, event_payload):
        x = json.loads(event_payload)
        metadata = FedAvgModelMetadata(**x)
        log_msg(f"EVENT: A model training started. modelId: {metadata.modelId}")
        self.modelId = metadata.modelId

    def training_finished(self, event_payload):
        log_msg("Training finiiiiiiiiiiiiiiished :D")
        log_msg(f"lead_aggregator_time_list = {time_list}")
        exit()

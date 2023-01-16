import json

import requests

from dto import EndRoundModel, AggregatedSecret, AggregatedSecretList
from gateway_rest_api import GatewayRestApi
from utils import log_msg, log_json
import time


class LeadAggregatorGatewayRestApi(GatewayRestApi):

    def __init__(self, base_url):
        super().__init__(base_url, '/leadAggregator')

    def get_personal_info(self):
        req_addr = self.prefix_url + '/getPersonalInfo'
        return self.get_personal_info_single(req_addr)

    def check_all_aggregated_secrets_received(self, model_id: str):
        log_msg("Check all aggregated secrets received...")

        req_addr = self.prefix_url + '/checkAllAggregatedSecretsReceived'
        params = {
            'modelId': model_id
        }

        resp = requests.get(req_addr, params=params)

        resp_json = {
            "address": req_addr,
            "status": str(resp)
        }
        log_json(resp_json)

        content = resp.content.decode()
        log_msg(f"Response: {content}")

        if content == "true":
            return True
        else:
            return False

    def add_end_round_model(self, body: EndRoundModel):
        log_msg("Add end round model...")

        req_addr = self.prefix_url + '/addEndRoundModel'
        response = requests.post(req_addr, json=body.to_map())

        resp_json = {
            "address": req_addr,
            "status": str(response),
            "time": str(time.time())
        }
        log_json(resp_json)

    def get_aggregated_secrets_for_current_round(self, model_id: str):
        log_msg("Sending get aggregated secrets for current round...")

        req_addr = self.prefix_url + '/getAggregatedSecretListForCurrentRound'
        params = {
            'modelId': model_id,
        }

        resp = requests.get(req_addr, params=params)

        resp_json = {
            "address": req_addr,
            "status": str(resp)
        }
        log_json(resp_json)

        content = resp.content.decode()
        aggregated_secret_list = AggregatedSecretList(**json.loads(content))

        my_list = []
        for item in aggregated_secret_list.aggregatedSecretList:
            aggregated_secret = AggregatedSecret(**item)
            log_msg("Has weight? YES" if aggregated_secret.weights is not None else "Has weight? NO")
            log_msg(f"Model Id: {aggregated_secret.modelId}")
            my_list.append(aggregated_secret)
        return my_list
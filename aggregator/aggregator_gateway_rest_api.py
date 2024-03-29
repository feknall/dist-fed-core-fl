import json
import requests

from dto import ModelSecretResponse, AggregatedSecret, \
    ModelSecretList
from gateway_rest_api import GatewayRestApi
from utils import log_msg, log_json
import time


class AggregatorGatewayRestApi(GatewayRestApi):

    def __init__(self, base_url):
        super().__init__(base_url, '/aggregator')

    def add_aggregated_secret(self, body: AggregatedSecret):
        log_msg("Adding aggregated secret...")

        req_addr = self.prefix_url + '/addAggregatedSecret'

        response = requests.post(req_addr, json=body.to_map())

        resp_json = {
            "address": req_addr,
            "status": str(response),
            "time": str(time.time())
        }
        log_json(resp_json)

    def get_model_secrets_for_current_round(self, model_id: str) -> list:
        log_msg("Sending reading model secrets for current round...")

        req_addr = self.prefix_url + '/getModelSecretListForCurrentRound'
        log_msg(f"Request address: {req_addr}")

        params = {
            'modelId': model_id
        }
        log_msg(f"Request params: {params}")

        resp = requests.get(req_addr, params=params)

        resp_json = {
            "address": req_addr,
            "status": str(resp)
        }
        log_json(resp_json)

        content = resp.content.decode()
        model_secret_list = ModelSecretList(**json.loads(content))

        my_list = []
        for item in model_secret_list.modelSecretList:
            secret = ModelSecretResponse(**item)
            log_msg("Has weight? YES" if secret.weights is not None else "Has weight? NO")
            log_msg(f"Model Id: {secret.modelId}")
            my_list.append(secret)
        return my_list

    def read_model_secrets(self, model_id: str):
        params = {
            'modelId': model_id,
            'round': round
        }
        req_addr = self.prefix_url + '/getModelSecretList'
        response = requests.get(req_addr, params=params)

        resp_json = {
            "address": req_addr,
            "status": str(response)
        }
        log_json(resp_json)

    def check_all_secrets_received(self, model_id: str):
        log_msg("Check all secrets received...")

        req_addr = self.prefix_url + '/checkAllSecretsReceived'

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
        if content == "true":
            return True
        else:
            return False

    def get_personal_info_aggregator(self):
        req_addr = self.prefix_url + '/getPersonalInfo'
        return self.get_personal_info_single(req_addr)

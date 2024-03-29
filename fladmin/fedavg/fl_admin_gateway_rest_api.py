import json
from typing import Union

import requests

from dto import ModelMetadata, EndRoundModel, FedAvgModelMetadata
from gateway_rest_api import GatewayRestApi
from utils import log_json, log_msg
import time


class FlAdminGatewayRestApi(GatewayRestApi):

    def __init__(self, base_url):
        super().__init__(base_url, '/fedAvg/flAdmin')

    def get_end_round_model(self, model_id: str) -> EndRoundModel:
        req_addr = self.prefix_url + '/getEndRoundModel'
        return super().get_end_round_model_base(model_id, req_addr)

    def init_ledger(self):
        req_addr = self.prefix_url + '/initLedger'
        response = requests.get(req_addr)

        resp_json = {
            "address": req_addr,
            "status": str(response)
        }
        log_json(resp_json)


    def create_model_metadata(self, body: Union[ModelMetadata, FedAvgModelMetadata]):
        log_msg("Sending creating a model metadata...")

        json_body = body.to_map()
        log_json(json_body)

        req_addr = self.prefix_url + '/createModelMetadata'
        resp = requests.post(req_addr, json=json_body)

        resp_json = {
            "address": req_addr,
            "status": str(resp)
        }
        log_json(resp_json)

        content = resp.content
        metadata = json.loads(content)

        log_msg("Response:")
        log_json(metadata)

    def start_training(self, model_id: str):
        log_msg("Sending start training...")

        req_addr = self.prefix_url + '/startTraining'
        params = {
            'modelId': model_id
        }
        log_json(params)

        resp = requests.post(req_addr, params=params)

        resp_json = {
            "address": req_addr,
            "status": str(resp),
            "time": str(time.time())
        }
        log_json(resp_json)

        content = resp.content
        metadata = json.loads(content)

        log_msg("Response:")
        log_json(metadata)

    def get_personal_info_fl_admin(self):
        req_addr = self.prefix_url + '/getPersonalInfo'
        return self.get_personal_info_single(req_addr)

    def check_has_fl_admin_attribute(self):
        log_msg('Checking user has fl admin attribute ...')

        req_addr = self.base_url + '/general/checkHasFlAdminAttribute'
        log_msg(f"Request address: {req_addr}")

        response = requests.get(req_addr)
        resp_json = {
            "address": req_addr,
            "status": str(response)
        }
        log_json(resp_json)

        content = response.content
        log_msg(f"Response: {content}")

        return content

import base64
import json
import time

import requests

from dto import PersonalInfo, EndRoundModel, OriginalModelRequest
from gateway_rest_api import GatewayRestApi
from utils import log_msg, log_json


class TrainerGatewayRestApi(GatewayRestApi):

    def __init__(self, base_url):
        super().__init__(base_url, '/fedAvg/trainer')

    def get_end_round_model(self, model_id: str) -> EndRoundModel:
        req_addr = self.prefix_url + '/getEndRoundModel'
        return super().get_end_round_model_base(model_id, req_addr)

    def add_original_model(self, body: OriginalModelRequest):
        log_msg("Sending secrets...")

        req_addr = self.prefix_url + '/addOriginalModel'
        response = requests.post(req_addr, json=body.to_map())

        resp_json = {
            "address": req_addr,
            "status": str(response),
            "time": str(time.time())
        }
        log_json(resp_json)

    def get_personal_info_trainer(self):
        log_msg("Getting personal info...")

        req_addr = self.prefix_url + '/getPersonalInfo'
        log_msg(f"Request address: {req_addr}")

        resp = requests.get(req_addr)

        resp_json = {
            "address": req_addr,
            "status": str(resp)
        }
        log_json(resp_json)

        content = resp.content.decode()

        personal_info_str_1 = json.loads(content)
        log_json(personal_info_str_1)

        personal_info_1 = PersonalInfo(**personal_info_str_1)

        return personal_info_1

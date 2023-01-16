import base64
import json

import requests

from dto import PersonalInfo, EndRoundModel
from dto import ModelSecretRequest
from gateway_rest_api import GatewayRestApi
from utils import log_msg, log_json
import time


class TrainerGatewayRestApi(GatewayRestApi):

    def __init__(self, base_url):
        super().__init__(base_url, '/trainer')

    def get_end_round_model(self, model_id: str) -> EndRoundModel:
        req_addr = self.prefix_url + '/getEndRoundModel'
        return super().get_end_round_model_base(model_id, req_addr)

    def add_model_secret(self, body: ModelSecretRequest):
        log_msg("Sending secrets...")

        req_addr = self.prefix_url + '/addModelSecret'
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
        a_list = json.loads(content)

        personal_info_str_1 = json.loads(base64.b64decode(a_list[0]))
        log_json(personal_info_str_1)

        personal_info_1 = PersonalInfo(**personal_info_str_1)

        personal_info_str_2 = json.loads(base64.b64decode(a_list[1]))
        log_json(personal_info_str_2)

        personal_info_2 = PersonalInfo(**personal_info_str_2)

        return personal_info_1, personal_info_2

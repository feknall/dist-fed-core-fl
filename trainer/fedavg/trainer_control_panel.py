from trainer.fedavg.trainer_gateway_rest_api import TrainerGatewayRestApi


class TrainerControlPanel:

    def __init__(self, gateway_rest_api: TrainerGatewayRestApi):
        self.gateway_rest_api = gateway_rest_api

    def get_personal_info(self):
        return self.gateway_rest_api.get_personal_info_trainer()

    def has_trainer_attribute(self):
        self.gateway_rest_api.check_has_trainer_attribute()

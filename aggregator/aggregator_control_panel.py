from aggregator.aggregator_gateway_rest_api import AggregatorGatewayRestApi


class AggregatorControlPanel:

    def __init__(self, gateway_rest_api: AggregatorGatewayRestApi):
        self.gateway_rest_api = gateway_rest_api

    def has_aggregator_attribute(self):
        self.gateway_rest_api.check_has_aggregator_attribute()

    def get_personal_info(self):
        self.gateway_rest_api.get_personal_info_aggregator()



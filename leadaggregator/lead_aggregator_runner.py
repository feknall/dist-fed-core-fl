import sys

from leadaggregator import lead_aggregator_event_listener as event_listener
from leadaggregator.lead_aggregator_control_panel import LeadAggregatorControlPanel
from leadaggregator.lead_aggregator_event_processor import LeadAggregatorEventProcessor
from leadaggregator.lead_aggregator_gateway_rest_api import LeadAggregatorGatewayRestApi


def run(address: str, port: str):
    gateway_rest_api = LeadAggregatorGatewayRestApi(f'http://{address}:{port}')
    websocket_address = f'ws://{address}:{port}'

    event_processor = LeadAggregatorEventProcessor(secrets_per_client=2, gateway_rest_api=gateway_rest_api)
    event_listener.listen(event_processor, websocket_address)

    control_panel = LeadAggregatorControlPanel(gateway_rest_api)
    control_panel.check_has_lead_aggregator_attribute()
    control_panel.get_personal_info()


if __name__ == "__main__":
    # trainer_runner.py [address] [port]
    # trainer_runner.py localhost 8082
    address = sys.argv[1]
    port = sys.argv[2]
    run(address, port)

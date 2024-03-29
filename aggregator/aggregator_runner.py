import sys

from aggregator.aggregator_event_processor import AggregatorEventProcessor
from aggregator.aggregator_gateway_rest_api import AggregatorGatewayRestApi
from aggregator.aggregator_control_panel import AggregatorControlPanel
from aggregator import aggregator_event_listener


def run(address: str, port: str):
    gateway_rest_api = AggregatorGatewayRestApi(f'http://{address}:{port}')
    websocket_address = f'ws://{address}:{port}'

    event_processor = AggregatorEventProcessor(gateway_rest_api=gateway_rest_api)
    aggregator_event_listener.listen(event_processor, websocket_address)

    control_panel = AggregatorControlPanel(gateway_rest_api)
    control_panel.has_aggregator_attribute()
    control_panel.get_personal_info()


if __name__ == "__main__":
    # aggregator_runner.py [address] [port]
    # aggregator_runner.py localhost 8091
    address = sys.argv[1]
    port = sys.argv[2]
    fed_avg = True
    run(address, port)

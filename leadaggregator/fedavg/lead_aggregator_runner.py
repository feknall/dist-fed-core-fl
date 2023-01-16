import asyncio
import sys

from leadaggregator.fedavg.lead_aggregator_gateway_rest_api import LeadAggregatorGatewayRestApi
from leadaggregator.fedavg.lead_aggregator_control_panel import LeadAggregatorControlPanel
from leadaggregator.fedavg import lead_aggregator_event_listener as event_listener
from leadaggregator.fedavg.lead_aggregator_event_processor import LeadAggregatorEventProcessor
from utils import log_msg


async def run(address: str, port: str):
    http_address = f'http://{address}:{port}'
    websocket_address = f'ws://{address}:{port}'
    log_msg(f"http_address: {http_address}")
    log_msg(f"websocket_address: {websocket_address}")

    gateway_rest_api = LeadAggregatorGatewayRestApi(http_address)

    event_processor = LeadAggregatorEventProcessor(gateway_rest_api=gateway_rest_api)
    event_listener.listen(event_processor, websocket_address)

    control_panel = LeadAggregatorControlPanel(gateway_rest_api)
    control_panel.check_has_lead_aggregator_attribute()
    control_panel.get_personal_info()


if __name__ == "__main__":
    # trainer_runner.py [address] [port]
    # trainer_runner.py localhost 8082
    address = sys.argv[1]
    port = sys.argv[2]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, port))

import asyncio
import sys

import trainer.fedavg.trainer_event_listener as event_listener
from trainer.fedavg.trainer_control_panel import TrainerControlPanel
from trainer.fedavg.trainer_event_processor import TrainerEventProcessor
from trainer.fedavg.trainer_gateway_rest_api import TrainerGatewayRestApi
from utils import log_msg


async def run(address: str, port: str, client_index: int):
    http_address = f'http://{address}:{port}'
    websocket_address = f'ws://{address}:{port}'
    log_msg(f"http_address: {http_address}")
    log_msg(f"websocket_address: {websocket_address}")

    gateway_rest_api = TrainerGatewayRestApi(http_address)

    event_processor = TrainerEventProcessor(client_index=client_index, gateway_rest_api=gateway_rest_api)
    event_listener.listen(event_processor, websocket_address)

    control_panel = TrainerControlPanel(gateway_rest_api)
    control_panel.has_trainer_attribute()
    control_panel.get_personal_info()


if __name__ == "__main__":
    # trainer_runner.py [address] [port] [client-index]
    # trainer_runner.py localhost 6001 1
    address = sys.argv[1]
    port = sys.argv[2]
    client_index = sys.argv[3]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, port, int(client_index)))

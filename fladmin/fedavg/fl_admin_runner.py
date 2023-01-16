import asyncio
import sys
import time

import fladmin.fedavg.fl_admin_event_listener as event_listener
from fladmin.fedavg.fl_admin_control_panel import FlAdminControlPanel
from fladmin.fedavg.fl_admin_event_processor import FlAdminEventProcessor
from fladmin.fedavg.fl_admin_gateway_rest_api import FlAdminGatewayRestApi
from utils import log_msg


async def run(address: str, port: str):
    http_address = f'http://{address}:{port}'
    websocket_address = f'ws://{address}:{port}'
    log_msg(f"http_address: {http_address}")
    log_msg(f"websocket_address: {websocket_address}")

    gateway_rest_api = FlAdminGatewayRestApi(http_address)

    event_processor = FlAdminEventProcessor(gateway_rest_api=gateway_rest_api)
    event_listener.listen(event_processor, websocket_address)

    control_panel = FlAdminControlPanel(gateway_rest_api)
    control_panel.has_fl_admin_attribute()
    control_panel.get_personal_info()
    control_panel.create_model_metadata()
    log_msg(f"Start training...")
    log_msg(f"Time: {time.time()}")
    control_panel.start_training()


if __name__ == "__main__":
    # trainer_runner.py [address] [port]
    # trainer_runner.py localhost 8083
    address = sys.argv[1]
    port = sys.argv[2]
    # address = 'localhost'
    # port = '8083'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, port))

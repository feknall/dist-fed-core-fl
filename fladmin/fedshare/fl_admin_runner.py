import time

from fladmin.fedshare.fl_admin_control_panel import FlAdminControlPanel
from fladmin.fedshare.fl_admin_event_processor import FlAdminEventProcessor
from fladmin.fedshare.fl_admin_gateway_rest_api import FlAdminGatewayRestApi
import fladmin.fedshare.fl_admin_event_listener as event_listener


def run(address: str, port: str):
    base = f'http://{address}:{port}'
    gateway_rest_api = FlAdminGatewayRestApi(base)
    websocket_address = f'ws://{address}:{port}'

    event_processor = FlAdminEventProcessor(gateway_rest_api=gateway_rest_api)
    event_listener.listen(event_processor, websocket_address)

    control_panel = FlAdminControlPanel(gateway_rest_api)
    control_panel.has_fl_admin_attribute()
    control_panel.get_personal_info()
    control_panel.create_model_metadata()
    print(f"Start training...")
    print(f"Time: {time.time()}")

    control_panel.start_training()


if __name__ == "__main__":
    # trainer_runner.py [address] [port]
    # trainer_runner.py localhost 8083
    # address = sys.argv[1]
    # port = sys.argv[2]
    address = 'localhost'
    port = '8083'
    run(address, port)

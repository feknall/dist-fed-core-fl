import sys
from trainer.fedshare.trainer_control_panel import TrainerControlPanel
from trainer.fedshare.trainer_gateway_rest_api import TrainerGatewayRestApi
from trainer.fedshare import trainer_event_listener
from trainer.fedshare.trainer_event_processor import TrainerEventProcessor


def run(address: str, port: str, client_index: int):
    http_address = f'http://{address}:{port}'
    websocket_address = f'ws://{address}:{port}'

    gateway_rest_api = TrainerGatewayRestApi(http_address)

    event_processor = TrainerEventProcessor(client_index=client_index, secrets_per_client=2,
                                            gateway_rest_api=gateway_rest_api)

    trainer_event_listener.listen(event_processor, websocket_address)
    control_panel = TrainerControlPanel(gateway_rest_api)
    control_panel.has_trainer_attribute()
    control_panel.get_personal_info()


if __name__ == "__main__":
    # trainer_runner.py [address] [port] [client-index]
    # trainer_runner.py localhost 6001 1
    address = sys.argv[1]
    port = sys.argv[2]
    client_index = sys.argv[3]
    run(address, port, int(client_index))

import asyncio
import threading

import websockets

from fladmin.fedshare.fl_admin_event_processor import FlAdminEventProcessor
from utils import log_msg
from info_pb2 import Event

AGGREGATION_FINISHED_EVENT = "AGGREGATION_FINISHED_EVENT"
ROUND_FINISHED_EVENT = "ROUND_FINISHED_EVENT"
TRAINING_FINISHED_EVENT = "TRAINING_FINISHED_EVENT"
MODEL_SECRET_ADDED_EVENT = "MODEL_SECRET_ADDED_EVENT"
CREATE_MODEL_METADATA_EVENT = "CREATE_MODEL_METADATA_EVENT"
START_TRAINING_EVENT = "START_TRAINING_EVENT"
ENOUGH_CLIENTS_CHECKED_IN_EVENT = "ENOUGH_CLIENTS_CHECKED_IN_EVENT"
AGGREGATED_SECRET_ADDED_EVENT = "AGGREGATED_SECRET_ADDED_EVENT"


async def process_socket_events(fl_admin: FlAdminEventProcessor, websocket_address):
    log_msg("Start listening to events...")
    async with websockets.connect(websocket_address) as websocket:
        async for message in websocket:
            event = Event()
            event.ParseFromString(message)
            print(event)
            event_name = event.name
            event_payload = event.payload
            if event_name == ROUND_FINISHED_EVENT:
                fl_admin.round_finished(event_payload)
            elif event_name == CREATE_MODEL_METADATA_EVENT:
                fl_admin.create_model_metadata(event_payload)
            elif event_name == START_TRAINING_EVENT:
                fl_admin.start_training_event(event_payload)
            elif event_name == TRAINING_FINISHED_EVENT:
                fl_admin.training_finished(event_payload)


def run(fl_admin: FlAdminEventProcessor, websocket_address):
    asyncio.run(process_socket_events(fl_admin, websocket_address))


def listen(fl_admin: FlAdminEventProcessor, websocket_address):
    thread = threading.Thread(target=run, args=(fl_admin, websocket_address))
    thread.start()

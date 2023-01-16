import asyncio

from utils import log_msg


async def x():
    log_msg("ouch")

loop = asyncio.get_event_loop()
loop.run_until_complete(x())
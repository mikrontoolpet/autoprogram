import asyncio

from autoprogram.errors import *

MAX_ATTEMPTS = 5
TIMEOUT = 600
WAIT_PERIOD = 1

def try_more_times(coro):
    async def wrapper(*args, **kwargs):
        attempt = 1
        successful = False
        while not successful and attempt <= MAX_ATTEMPTS:
            try:
                res = await asyncio.wait_for(coro(*args, **kwargs), TIMEOUT)
                return res
                successful = True
            except Exception:
                attempt += 1
            await asyncio.sleep(WAIT_PERIOD)

        if attempt > MAX_ATTEMPTS:
            raise TryMoreTimesFailed
    return wrapper
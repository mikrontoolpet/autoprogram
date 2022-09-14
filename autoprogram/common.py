import asyncio
import logging

from autoprogram.errors import *

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def try_more_times(max_attempts=5, timeout=600, wait_period=1, retry_exception=Exception):
    """
    This decorator tries mor time to await a coroutine in case of a specific
    exception, given a timeout and a retry period.
    Another version should be created, with a stop exception
    """
    def decorator(coro):
        async def wrapper(*args, **kwargs):
            attempt = 1
            successful = False

            while (not successful) and (attempt <= max_attempts):
                try:
                    res = await asyncio.wait_for(coro(*args, **kwargs), timeout)
                    successful = True
                    return res
                except retry_exception as e:
                        _logger.error(f"Exception {e.args} encountered, retry...")
                attempt += 1
                await asyncio.sleep(wait_period)

            if attempt > max_attempts:
                raise TryMoreTimesFailed
        return wrapper
    return decorator
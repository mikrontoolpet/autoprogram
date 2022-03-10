import asyncio
import logging

from autoprogram.errors import *

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def try_more_times(max_attempts=5, timeout=600, wait_period=1, retry_exception=Exception):
    """
    This decorator tries mor time to await a coroutine in case of a specific
    exception, given a timeout and a retry period.
    """
    def decorator(coro):
        async def wrapper(*args, **kwargs):
            attempt = 1
            successful = False

            while not successful and attempt <= max_attempts:
                try:
                    res = await asyncio.wait_for(coro(*args, **kwargs), timeout)
                    return res
                    successful = True
                except retry_exception as e:
                    attempt += 1
                    _logger.error(e)
                await asyncio.sleep(wait_period)

            if attempt > max_attempts:
                raise TryMoreTimesFailed
        return wrapper
    return decorator
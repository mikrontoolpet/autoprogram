import asyncio
from pathlib import Path
import win32com.client
import logging

from autoprogram.errors import *

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def try_more_times(max_attempts=5, timeout=6000, wait_period=1, retry_exception=Exception):
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
                    res = await asyncio.wait_for(coro(*args, **kwargs), timeout) # run coroutine with a timeout
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

def full_pathlib_path(parent_dir, file_name, suffix):
    """
    This method returns the full pathlib path, given the file name,
    its parent directory and its suffix
    """
    return Path(parent_dir).joinpath(file_name + suffix)

def create_shortcut(source_raw_path, shortcut_raw_path):
    source_path = str(source_raw_path)
    shortcut_path = str(shortcut_raw_path)
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = source_path
    shortcut.IconLocation = source_path
    shortcut.Save()
    _logger.info("Wheelpack PNG shortcut created!!!")

def create_res_shortcut_from_file_name(parent_dir, file_name, file_suffix, res_prog_dir):
    pthlb_source_full_path = full_pathlib_path(parent_dir, file_name, file_suffix)
    pthlb_shortcut_path = Path(res_prog_dir).joinpath(file_name + ".lnk")
    create_shortcut(pthlb_source_full_path, pthlb_shortcut_path)

def is_nan(val):
    return val != val
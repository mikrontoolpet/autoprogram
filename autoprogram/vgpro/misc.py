import asyncio
import re


ADD_CHARS = "[°¦m¦mm¦s¦/¦min¦%¦ ]"


class ApplicationState:
	"""
	This class contain class variables
	corresponding to more readable
	vgp application states
	"""
	unknown = 0
	ready = 1
	processing = 2
	waiting = 3


class ConnectionState:
    """
    This class contain class variables
    corresponding to more readable
    opc server connection states
    """
    down = 0
    up = 1


class ApplicationStateHandler(object):
    """
    Subscription handler that sets the class variable
    ApplicationStateHandler.app_state equal to the subscribed
    node (the application state node)
    """
    app_state = 0
    
    def datachange_notification(self, node, val, data):
        ApplicationStateHandler.app_state = val


def wait_till_ready(coro):
    """
    Wait till ready decorator
    """
    async def wrapper(*args, **kwargs):
        print("Awaiting coroutine " + coro.__name__ +  "...", flush=True)
        res = await coro(*args, **kwargs)
        await asyncio.sleep(0.12)
        while ApplicationStateHandler.app_state != ApplicationState.ready:
            # print("Application state: ", ApplicationStateHandler.app_state, flush=True)
            await asyncio.sleep(0.12)
        print("Coroutine " + coro.__name__ + " awaited!", flush=True)
        return res
    return wrapper


def vgp_str_to_float(vgp_str_val):
    str_val = re.sub(ADD_CHARS, "",vgp_str_val)
    res = float(str_val)
    return res
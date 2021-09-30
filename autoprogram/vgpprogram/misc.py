import asyncio

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
        res = await coro(*args, **kwargs)
        await asyncio.sleep(0.12)
        while ApplicationStateHandler.app_state != ApplicationState.ready:
            # print("Application state: ", ApplicationStateHandler.app_state,\
            # flush=True)
            await asyncio.sleep(0.12)
        # try:
        #     print(coro.__str__()," with arg ", args[1]," done!", flush=True)
        # except IndexError:
        #     print(coro.__str__(), " done!", flush=True)
        return res
    return wrapper
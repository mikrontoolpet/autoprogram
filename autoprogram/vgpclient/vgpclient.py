import asyncio
import re

from asyncua import Client, ua
from .misc import ApplicationState


class ApplicationStateHandler(object):
    """
    Subscription handler that sets the class variable
    ApplicationStateHandler.app_state equal to the subscribed
    node (the application state node)
    """
    app_state = 0
    
    def datachange_notification(self, node, val, data):
        ApplicationStateHandler.app_state = val

# def wait_till_ready_after(coro):
#     """
#     This decorator executes the coroutine "coro"and then
#     waits until the variable ApplicationStateHandler.app_state
#     becomes 1 (ApplicationState.ready)
#     """
#     async def wrapper(*args, **kwargs):
#         res = await coro(*args, **kwargs)
#         while ApplicationStateHandler.app_state != ApplicationState.ready:
#             # print("Application state: ", ApplicationStateHandler.app_state, flush=True)
#             await asyncio.sleep(0.1)
#         return res # the result from the coro() method must be returned, if any
#     return wrapper

def wait_till_ready(coro):
    """
    Wait till ready decorator
    """
    async def wrapper(*args, **kwargs):
        res = await coro(*args, **kwargs)
        while ApplicationStateHandler.app_state != ApplicationState.ready:
            # print("Application state: ", ApplicationStateHandler.app_state, flush=True)
            await asyncio.sleep(0.1)
        return res
    return wrapper


class VgpClient:

    def __init__(self, url):
        """
        Create an instance of the Client class
        """
        self.client = Client(url, timeout=20)

    async def __aenter__(self):
        """
        Append the subscription to the application state node
        after the Client __aenter__method
        """
        await self.client.__aenter__()
        app_state_node = self.client.get_node("ns=2;s=ProgramMetadata/ApplicationState")
        handler = ApplicationStateHandler()
        sub = await self.client.create_subscription(500, handler)
        handle = await sub.subscribe_data_change(app_state_node)
        return self # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Just call the Client __aexit__ method
        """
        await self.client.__aexit__(exc_type, exc_value, traceback)

    @wait_till_ready
    async def load_tool(self, path):
        """
        Method that loads the specified .vgp file
        """
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("LoadFile", path)

    @wait_till_ready
    async def save_tool(self, path):
        """
        Method that saves the .vgp file with the specified filename
        """
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("SaveFile", path)

    @wait_till_ready
    async def get(self, nodeid):
        """
        Get the value at the specified node id. If the value is a float,
        additional string characters are stripped and then it's converted
        to float. If the stripped string is not convertible to float, it's
        left as a raw string
        """
        node = self.client.get_node(nodeid)
        raw_str_val = await node.read_value()
        str_val = re.sub("[^-.0-9]", "",raw_str_val)
        try:
            res = float(str_val)
        except ValueError:
            res = raw_str_val
        return res

    @wait_till_ready
    async def set(self, nodeid, raw_val):
        """
        Set the value after formatting the input to the correct opc-ua
        data type
        """
        node = self.client.get_node(nodeid) # get the specified node object
        ua_type = await node.read_data_type_as_variant_type() # get the right opc-ua type to which the input value must be formatted
        """
        Since python float and int types cannot be formatted to ua.VariantType.String
        (an AttributeError is thrown), when the Exception is raised, the raw input
        value is conveted to str before being formatted to ua.VariantType.String
        """
        try:
            ua_val = ua.Variant(raw_val, ua_type) # format the input value with the correct opc-ua type
            await node.write_value(ua_val)
        except AttributeError:
            raw_str_val = str(raw_val)
            ua_val = ua.Variant(raw_str_val, ua_type)
            await node.write_value(ua_val)

    @wait_till_ready
    async def close_file(self):
        """
        Method that closes the .vgp file
        """
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("CloseFile")
import asyncio
import logging
import re

from asyncua import Client, ua
from pathlib import Path


SERVER_URL = "opc.tcp://localhost:8996/"
DEC_DIGITS = 3
ADD_CHARS = "[°¦m¦mm¦s¦/¦min¦%¦ ]"


# Set logging level to ERROR in order to silence warning messages from asyncua
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


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


class VgpClient:
    def __init__(self):
        """
        Create an instance of the Client class
        """
        self.client = Client(SERVER_URL, timeout=120)

    async def __aenter__(self):
        """
        Append the subscription to the application state node
        after the Client __aenter__method
        """
        print("Connecting to OPC-UA server...", flush=True)
        await self.wait_for_connection()
        await self.create_data_change_subscription("ns=2;s=ProgramMetadata/ApplicationState", ApplicationStateHandler())
        print("Connected to OPC-UA server!", flush=True)
        return self # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Just call the self.client __aexit__ method
        """
        print("Disonnecting from OPC-UA server...", flush=True)
        await self.client.__aexit__(exc_type, exc_value, traceback)
        print("Disconnected from OPC-UA server!", flush=True)

    async def _wait_for_connection(self):
        """
        This method tries to connect to the OPC-UA server started from the
        VgPro application, until the connection is succesful
        """
        ready_to_connect = ConnectionState.down
        while ready_to_connect != ConnectionState.up:
            try:
                await self.client.__aenter__()
                ready_to_connect = ConnectionState.up
            except ConnectionRefusedError:
                pass
            except ua.uaerrors._auto.BadServerHalted:
                pass


    async def wait_for_connection(self, timeout=60):
        """
        This method calls self._wait_for_connection() with a timeout, if
        the timout is exceeded, a TimeoutError is raised.
        """
        try:
            await asyncio.wait_for(self._wait_for_connection(), timeout)
        except asyncio.TimeoutError:
            raise self.error_list(2)


    @wait_till_ready
    async def create_data_change_subscription(self, nodeid, handler, sub_period=100):
        """
        Create a subscription to a data change of the selected node
        """
        app_state_node = self.client.get_node(nodeid)
        sub = await self.client.create_subscription(sub_period, handler)
        handle = await sub.subscribe_data_change(app_state_node)

    @wait_till_ready
    async def load_tool(self, raw_path):
        """
        Method that loads the specified .vgp file
        """
        str_path = str(raw_path)
        ua_str_path = ua.Variant(str_path, ua.VariantType.String)
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("LoadFile", ua_str_path)

    @wait_till_ready
    async def save_tool(self, raw_path):
        """
        Method that saves the .vgp file with the specified filename. If
        the specified path already exists, the file is deleted before beeing
        resaved, otherwise VgPro raises an error.
        """
        pthl_path = Path(raw_path)
        if pthl_path.is_file():
            pthl_path.unlink()
        str_path = str(raw_path)
        ua_str_path = ua.Variant(str_path, ua.VariantType.String)
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("SaveFile", ua_str_path)

    @wait_till_ready
    async def delete_all_flanges(self):
        """
        Method that removes all flanges, used to allow faster calculations
        """
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("DeleteAllFlanges")

    @wait_till_ready
    async def load_wheel(self, raw_whp_path, whp_posn):
        """
        Method that loads the selected wheelpack in a specified position (BUGGED).
        It converts to python int before converting to ua.VariantType.Int,
        matching the index with the position.
        """
        str_whp_path = str(raw_whp_path)
        int_whp_posn = int(whp_posn) - 1
        ua_str_whp_path = ua.Variant(str_whp_path, ua.VariantType.String)
        ua_int_whp_posn = ua.Variant(int_whp_posn, ua.VariantType.Int32)
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("LoadWheels", ua_str_whp_path, ua_int_whp_posn)

    @wait_till_ready
    async def load_iso_easy(self, raw_path):
        """
        Method that deletes all the previous iso programs and loads the
        specified iso easy program.
        """
        str_path = str(raw_path)
        ua_str_path = ua.Variant(str_path, ua.VariantType.String)
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        try:
            await self.delete_all_iso()
            await parent_node.call_method("LoadIsoEasy", ua_str_path)
        except ua.uaerrors._auto.Bad:
            self.error_list(4)

    @wait_till_ready
    async def delete_all_iso(self):
        """
        Method that removes all iso easy programs
        """
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("DeleteAllIso")

    @wait_till_ready
    async def close_file(self):
        """
        Method that closes the .vgp file
        """
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("CloseFile")

    @wait_till_ready
    async def get(self, nodeid):
        """
        1) Read the value as it is
        2) Try to convert to float, otherwise leave it as it is
        """
        try:
            print(f"Get method called with argument: {str(nodeid)}")
            node = self.client.get_node(nodeid)
            ua_type = await node.read_data_type_as_variant_type()
            val = await node.read_value() # value already read with python format (e.g. float, str, ...)
            vgp_str_val = str(val)
            try:
                res = self.vgp_str_to_float(vgp_str_val)
            except ValueError:
                res = vgp_str_val
            print(f"Parameter at {str(nodeid)} read with value {res}.")
            return res
        except ua.uaerrors._auto.BadNodeIdUnknown:
            self.error_list(3)
        except ua.uaerrors._auto.BadAttributeIdInvalid:
            self.error_list(5)

    @wait_till_ready
    async def set(self, nodeid, raw_val):
        """
        Set the value after formatting the input to the correct opc-ua
        data type:
        1) Convert the raw input to string value
        2) Try to format it to a float (stripping additional chars and
           rounding it), otherwise is left as it is
        3) Depending on the target OPC-UA type, the value (float or string)
           is converted to a python native suitable for the following
           formatting to an OPC-UA type
        4) The value is formatted to an OPC-UA type
        """
        str_val = str(raw_val)
        try:
            val = self.vgp_str_to_float(str_val)
        except ValueError:
            val = str_val
        node = self.client.get_node(nodeid) # get the specified node object
        try:
            ua_type = await node.read_data_type_as_variant_type()
            if ua_type == ua.VariantType.Int32:
                int_val = int(val)
                ua_val = ua.Variant(int_val, ua_type)
            elif ua_type == ua.VariantType.Double:
                float_val = float(val)
                ua_val = ua.Variant(float_val, ua_type)
            elif ua_type == ua.VariantType.String:
                str_val = str(val)
                ua_val = ua.Variant(str_val, ua_type)
            elif ua_type == ua.VariantType.Boolean:
                str_val = str(val)
                ua_val = ua.Variant(str_val, ua_type) # ua.VariantType.Boolean supports python string type
            else:
                raise self.error_list(0)
            await node.write_value(ua_val)
            print(f"Parameter at {str(nodeid)} set with value {str(ua_val.Value)}.")
        except ValueError:
            self.error_list(1)
        except ua.uaerrors._auto.BadNodeIdUnknown:
            self.error_list(3)
        except ua.uaerrors._auto.BadAttributeIdInvalid:
            self.error_list(5)

    @wait_till_ready
    async def calculate_cycle_time(self):
        """
        Method that calculates cycle time
        """
        parent_node = self.client.get_node("ns=2;s=Commands/Simulation")
        await parent_node.call_method("CalculateCycleTime")

    @staticmethod
    def vgp_str_to_float(vgp_str_val):
        str_val = re.sub(ADD_CHARS, "",vgp_str_val)
        try:
            res = round(float(str_val),DEC_DIGITS)
        except ValueError:
             raise ValueError(f"Value not convertible to float: {vgp_str_val}")
        return res

    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            raise TypeError("Python type not compatible with UA type.")
        elif err_id == 1:
            raise ValueError("Value not suitable for OPC-UA type formatting.")
        elif err_id == 2:
            raise TimeoutError("Connection attempt took too long, program ends.")
        elif err_id == 3:
            raise ValueError("Bad node id.")
        elif err_id == 4:
            raise ValueError("Bad iso easy path.")
        elif err_id == 5:
            raise ValueError("This node hasn't any type.")
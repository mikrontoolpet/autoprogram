import asyncio
import logging
import re

# Set asyncua logging level to WARNING in order to not visualize INFO messages
logging.getLogger('asyncua').setLevel(logging.WARNING)
from asyncua import Client, ua
from pathlib import Path
from autoprogram.dbhandler import DataBase


SERVER_URL = "opc.tcp://localhost:8996/"
DEC_DIGITS = 3
ADD_CHARS = "[°¦m¦mm¦s¦/¦min¦%¦ ]"
WHP_POSN_ARGS = ("VGP_Guid", "G_Type", "Rollomatic.Common.MetaLibrary.Flange", "G_Position")

SUB_PERIOD = 100 # [ms], the variable ApplicationStateHandler.app_state is read and updated every <SUB_PERIOD> milliseconds (server communication cycle time)
APP_STATE_CHECK_PERIOD = 0.15 # [s], while waiting the application to be ready, the ApplicationStateHandler.app_state is checked every <APP_STATE_CHECK_PERIOD> seconds
APP_STATE_INIT_WAIT_TIME = 0.2 # [s], initial time to let the ApplicationStateHandler.app_state to change value (must be higher than APP_STATE_CHECK_PERIOD)
# APP_STATE_CHECK_PERIOD_WHEEL = 0.5 # [s], while waiting the application to be ready, the ApplicationStateHandler.app_state is checked every <APP_STATE_CHECK_PERIOD> seconds
# APP_STATE_INIT_WAIT_TIME_WHEEL = 1 # [s], initial time to let the ApplicationStateHandler.app_state to change value (must be higher than APP_STATE_CHECK_PERIOD)

REQUEST_TIMEOUT = 120 # [s], it's the max time a connection can last
CONNECTION_START_ATTEMPT_TIMEOUT = 60 # [s], it's the max time the connection is attempted to be started
CONNECTION_START_ATTEMPT_PERIOD = 1 # [s]


# Set vgpclient logging level to INFO
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


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
    Await the argument coroutine "coro" and then wait that the application
    state is ready
    """
    async def wrapper(*args, **kwargs):
        _logger.info("Awaiting coroutine " + coro.__name__ +  "...")
        res = await coro(*args, **kwargs)
        await asyncio.sleep(APP_STATE_INIT_WAIT_TIME)
        while ApplicationStateHandler.app_state != ApplicationState.ready:
            # _logger.info("Application state: " + str(ApplicationStateHandler.app_state))
            await asyncio.sleep(APP_STATE_CHECK_PERIOD)
        _logger.info("Coroutine " + coro.__name__ + " awaited!")
        return res
    return wrapper


class VgpClient:
    def __init__(self):
        self.client = Client(SERVER_URL, timeout=REQUEST_TIMEOUT)
        self.app_state_sub = None

    async def __aenter__(self):
        """
        Open the VgPro application, start the OPC-UA client connection to the
        server and make the subscription to the ApplicationState node
        """
        await self.start_connection()
        self.app_state_sub = await self.create_data_change_subscription("ns=2;s=ProgramMetadata/ApplicationState", ApplicationStateHandler())
        return self # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Delete application state subscription, close the connection to the
        server and closethe VgPro application
        """
        await self.delete_data_change_subscription(self.app_state_sub)
        await self.close_connection(exc_type, exc_value, traceback)

    async def _start_connection(self):
        """
        This method tries to connect to the OPC-UA server started from the
        VgPro application, until the connection is succesful
        """
        _logger.info("Connecting to OPC-UA server...")
        ready_to_connect = ConnectionState.down
        while ready_to_connect != ConnectionState.up:
            try:
                await self.client.__aenter__()
                ready_to_connect = ConnectionState.up
            except ConnectionRefusedError:
                pass
            except ua.uaerrors._auto.BadServerHalted:
                pass
            await asyncio.sleep(CONNECTION_START_ATTEMPT_PERIOD)
        _logger.info("Connected to OPC-UA server!")

    async def start_connection(self):
        """
        This method calls self._start_connection() with a timeout, if
        the timeout is exceeded, a TimeoutError is raised.
        """
        try:
            await asyncio.wait_for(self._start_connection(), CONNECTION_START_ATTEMPT_TIMEOUT)
        except asyncio.TimeoutError:
            self.error_list(2)

    async def create_data_change_subscription(self, nodeid, handler):
        """
        Create a subscription to a data change of the selected node, giving a
        cycle time for the server variable reading
        """
        _logger.info("Creating subscription to the node " + str(nodeid) + "...")
        subscription = await self.client.create_subscription(SUB_PERIOD, handler)
        subscription_node = [self.client.get_node(nodeid)]
        await subscription.subscribe_data_change(subscription_node)
        _logger.info("Subscription to the node " + str(nodeid) + " created!")
        return subscription

    async def close_connection(self, exc_type, exc_value, traceback):
        """
        Close OPC-UA connection
        """
        _logger.info("Disonnecting from OPC-UA server...")
        await self.client.__aexit__(exc_type, exc_value, traceback)
        _logger.info("Disconnected from OPC-UA server!")

    async def delete_data_change_subscription(self, subscription):
        """
        Delete the data change subscription passed as argument
        """
        await subscription.delete()

    @wait_till_ready
    async def load_tool(self, raw_path):
        """
        Method that loads the specified .vgp file
        """
        pthlb_path = Path(raw_path)
        if not pthlb_path.is_file():
            self.error_list(6, raw_path)
        else:
            str_path = str(raw_path)
            ua_str_path = ua.Variant(str_path, ua.VariantType.String)
            parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
            try:
                await parent_node.call_method("LoadFile", ua_str_path)
            except ua.uaerrors._auto.Bad:
                self.error_list(6, str_path)
            _logger.info(f"File loaded: {str_path}")


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

        # Read the default wheelpack position
        with DataBase(str_whp_path) as whp_db:
            default_int_whp_posn = int(whp_db[WHP_POSN_ARGS])
        # Shift the wheelpack position in order to have the desired position
        whp_posn_shift = int_whp_posn - default_int_whp_posn

        # Convert to ua-types
        ua_str_whp_path = ua.Variant(str_whp_path, ua.VariantType.String)
        ua_whp_posn_shift = ua.Variant(whp_posn_shift, ua.VariantType.Int32)
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("LoadWheels", ua_str_whp_path, ua_whp_posn_shift)

    @wait_till_ready
    async def load_isoeasy(self, raw_path):
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
            self.error_list(4, str_path)

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
    async def read(self, nodeid):
        """
        1) Read the value as it is
        2) Try to convert to float, otherwise leave it as it is
        """
        try:
            _logger.info(f"Get method called with argument: {str(nodeid)}")
            node = self.client.get_node(nodeid)
            ua_type = await node.read_data_type_as_variant_type()
            val = await node.read_value() # value already read with python format (e.g. float, str, ...)
            vgp_str_val = str(val)
            try:
                res = self.vgp_str_to_float(vgp_str_val)
            except ValueError:
                res = vgp_str_val
            _logger.info(f"Parameter at {str(nodeid)} read with value {res}.")
            return res
        except ua.uaerrors._auto.BadNodeIdUnknown:
            self.error_list(3, nodeid)
        except ua.uaerrors._auto.BadAttributeIdInvalid:
            self.error_list(5, nodeid)

    @wait_till_ready
    async def write(self, nodeid, raw_val):
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
                raise self.error_list(0, ua_type)
            await node.write_value(ua_val)
        except ValueError:
            self.error_list(1, nodeid)
        except ua.uaerrors._auto.BadNodeIdUnknown:
            self.error_list(3, nodeid)
        except ua.uaerrors._auto.BadAttributeIdInvalid:
            self.error_list(5, nodeid)
        _logger.info(f"Parameter at {str(nodeid)} set with value {str(ua_val.Value)}.")

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
            res = round(float(str_val), DEC_DIGITS)
        except ValueError:
             raise ValueError(f"Value not convertible to float: {vgp_str_val}")
        return res

    def error_list(self, err_id, *args, **kwargs):
        """
        In case of error
        """
        if err_id == 0:
            raise TypeError(f"Type {args[0]} not compatible with any of UA types.")
        elif err_id == 1:
            raise ValueError(f"Value at node {args[0]} not suitable for OPC-UA type formatting.")
        elif err_id == 2:
            raise TimeoutError("Connection attempt took too long, program ends.")
        elif err_id == 3:
            raise ValueError(f"Bad node id: {args[0]}")
        elif err_id == 4:
            raise ValueError(f"Bad isoeasy path: {args[0]}")
        elif err_id == 5:
            raise ValueError(f"The value at node {args[0]} hasn't any type")
        elif err_id == 6:
            raise ValueError(f"No such a file: {args[0]}")
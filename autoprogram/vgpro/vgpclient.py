import asyncio
import logging

from asyncua import Client, ua
from pathlib import Path
from autoprogram.vgpro.misc import ConnectionState, ApplicationStateHandler, wait_till_ready

# Set logging level to ERROR in order to silence warning messages from asyncua
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class VgpClient:
    def __init__(self, url):
        """
        Create an instance of the Client class
        """
        self.client = Client(url, timeout=120)

    async def __aenter__(self):
        """
        Append the subscription to the application state node
        after the Client __aenter__method
        """
        ready_to_connect = 0
        await self.wait_for_connection()
        await self.create_data_change_subscription("ns=2;s=ProgramMetadata/ApplicationState", ApplicationStateHandler())
        return self # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Just call the self.client __aexit__ method
        """
        await self.client.__aexit__(exc_type, exc_value, traceback)

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
    async def close_file(self):
        """
        Method that closes the .vgp file
        """
        parent_node = self.client.get_node("ns=2;s=Commands/FileManagement")
        await parent_node.call_method("CloseFile")

    @wait_till_ready
    async def get(self, nodeid):
        """
        Get the value at the specified node id. If the value is a float,
        additional string characters are stripped and then it's converted
        to float. If the stripped string is not convertible to float, it's
        left as a raw string
        """
        node = self.client.get_node(nodeid)
        ua_type = await node.read_data_type_as_variant_type()
        ua_val = await node.read_value()
        res = str(ua_val)
        return res

    @wait_till_ready
    async def set(self, nodeid, raw_val):
        """
        Set the value after formatting the input to the correct opc-ua
        data type:
        1) Get the right opc-ua type to which the input value must be formatted
        2) Depending on the target OPC-UA type, the raw value is converted
           from python native type to OPC-UA type
        """
        node = self.client.get_node(nodeid) # get the specified node object
        ua_type = await node.read_data_type_as_variant_type()
        try:
            if ua_type == ua.VariantType.Int32:
                int_val = int(raw_val)
                ua_val = ua.Variant(int_val, ua_type)
            elif ua_type == ua.VariantType.Double:
                float_val = float(raw_val)
                ua_val = ua.Variant(float_val, ua_type)
            elif ua_type == ua.VariantType.String:
                str_val = str(raw_val)
                ua_val = ua.Variant(str_val, ua_type)
            else:
                raise self.error_list(0)
            await node.write_value(ua_val)
        except ValueError:
            raise self.error_list(1)
        
    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            return TypeError("Python type not compatible with UA type.")
        elif err_id == 1:
            return ValueError("Value not suitable for OPC-UA type formatting.")
        elif err_id == 2:
            return TimeoutError("Connection attempt took too long, program ends.")
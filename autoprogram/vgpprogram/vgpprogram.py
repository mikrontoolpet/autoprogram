import re

from asyncua import Client, ua
from pathlib import Path
from autoprogram.vgpprogram.misc import ApplicationStateHandler, wait_till_ready

class VgpProgram:
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
        await self.client.__aenter__()
        await self.create_data_change_subscription("ns=2;s=ProgramMetadata/ApplicationState", ApplicationStateHandler())
        return self # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Just call the self.Client __aexit__ method
        """
        await self.client.__aexit__(exc_type, exc_value, traceback)

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
        Method that saves the .vgp file with the specified filename
        """
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
        data type:
        1) Get the right opc-ua type to which the input value must be formatted
        2) Since python float and int types cannot be formatted to
           ua.VariantType.String (an AttributeError is thrown), when the
           Exception is raised, the raw input value is converted to str
           before being formatted to ua.VariantType.String
        3) Try to format the input value (int or float) with the correct opc-ua
           type (ua.VariantType.Int or ua.VariantType.Double, respectively)
        4) If an AttributeErrore is raised, it formats the input value as
           ua.VariantType.String (not necessary, since python str already
           fits the correspondent ua string
        """
        node = self.client.get_node(nodeid) # get the specified node object
        ua_type = await node.read_data_type_as_variant_type()
        try:
            ua_val = ua.Variant(raw_val, ua_type)
            await node.write_value(ua_val)
        except AttributeError:
            raw_str_val = str(raw_val)
            ua_val = ua.Variant(raw_str_val, ua_type)
            await node.write_value(ua_val)
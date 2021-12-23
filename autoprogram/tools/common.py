import re
from pathlib import Path

from autoprogram.wbhandler import WorkBook
from autoprogram.config import Config


class Meta(type):
    """
    Metaclass defined in order to assess that the tool classes have the
    family_address class variable
    """
    def __new__(cls, name, bases, body):
        print("Creating class " + str(name) + "...", flush=True)
        if name != "BaseTool":
            if not "family_address" in body:
                raise AttributeError("Tool class without family_address class attribute.")
            if not "set_parameters" in body:
                raise AttributeError("Tool class without set_parameters method.")
            if not "set_wheels" in body:
                raise AttributeError("Tool class without set_wheels method.")
            if not "set_isoeasy" in body:
                raise AttributeError("Tool class without set_isoeasy method.")
        return super().__new__(cls, name, bases, body)


class BaseTool(metaclass=Meta):

    def __init__(self, vgp_client, name, family_address):
        self.name = name
        self.vgpc = vgp_client # active VgpClient instance (whose __aenter__ method has been run)
        self.master_prog_path = Path(Config.MASTER_PROGS_BASE_DIR).joinpath(family_address, Config.MASTER_PROG_NAME + Config.VGP_SUFFIX)
        self.res_prog_path = Path(Config.RES_PROGS_DIR).joinpath(name + Config.VGP_SUFFIX)
        self.std_whp_base_dir = Config.STD_WHP_BASE_DIR
        self.whp_suffix = Config.WHP_SUFFIX
        self.common_wb = WorkBook("C:/Users/0gugale/Desktop/master_progs_base_dir/common/common.xlsx")

    async def __aenter__(self):
        """
        This __aenter__() method performs the following tasks:
        1) Load the correct master program
        2) Save the program on the local machine
        """
        await self.vgpc.load_tool(self.master_prog_path)
        await self.vgpc.save_tool(self.res_prog_path)
        await self.vgpc.delete_all_flanges()
        return self # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        This __aexit__() method performs the following tasks:
        1) Save the program
        2) Close the file
        """
        await self.vgpc.save_tool(self.res_prog_path)
        await self.vgpc.close_file()

    def check_boundary(self, arg, low_bound, up_bound):
        """
        This method raises an error if the argument value is not between the
        lower and the upper boundaries
        """
        if arg < low_bound or arg > up_bound:
            self.error_list(0)

    def full_whp_path(self, whp_name):
        """
        This method return the wheelpack full path, given its name
        """
        pthlb_whp_path = Path(self.std_whp_base_dir).joinpath(whp_name + self.whp_suffix)
        str_whp_path = str(pthlb_whp_path)
        return str_whp_path

    async def create(self):
        """
        Wrap the three methods necessary to create the tool
        """
        await self.set_parameters()
        await self.set_wheels()
        await self.set_isoeasy()

    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            raise ValueError("The input argument is out of boundary.")
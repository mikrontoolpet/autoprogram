import shutil
from pathlib import Path

from autoprogram.wbhandler import WorkBook
from autoprogram.config import Config


class Meta(type):
    """
    Metaclass defined in order to assess that the tool classes have the
    family_address class variable
    """
    def __new__(cls, name, bases, body):
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

    def __init__(self, machine, vgp_client, name, family_address):
        self.machine = machine
        self.vgpc = vgp_client # active VgpClient instance (whose __aenter__ method has been run)
        self.name = name
        self.family_address = family_address

    async def __aenter__(self):
        """
        This __aenter__() method performs the following tasks:
        1) Create shortcuts and workbooks (DataFrames)
        2) Copies the master program on the local machine
        3) Load the correct master program
        4) Save the program on the local machine
        """
        self.family_dir = Path(Config.MASTER_PROGS_BASE_DIR).joinpath(self.family_address)
        self.complete_name = self.name + "_" + self.machine
        self.res_prog_dir = Path(Config.RES_PROGS_DIR).joinpath(self.complete_name)
        self.res_prog_dir.mkdir(parents=True, exist_ok=True)
        self.master_prog_path = self.family_dir.joinpath(Config.MASTER_PROG_DIR, Config.MASTER_PROG_NAME + "_" + self.machine + Config.VGP_SUFFIX)
        self.res_prog_path = self.res_prog_dir.joinpath(self.complete_name + Config.VGP_SUFFIX)
        self.common_wb_path = Path(Config.MASTER_PROGS_BASE_DIR).joinpath(Config.COMMON_FILE_DIR, Config.COMMON_FILE_NAME)
        self.common_wb = WorkBook(self.common_wb_path)
        self.worksheets_dir = self.family_dir.joinpath(Config.WORKSHEETS_DIR)
        self.isoeasy_dir = self.family_dir.joinpath(Config.ISOEASY_DIR)
        self.configuration_wb_path = self.worksheets_dir.joinpath(Config.CONFIG_FILE_NAME)
        self.configuration_wb = WorkBook(self.configuration_wb_path)
        self.std_whp_base_dir = Config.STD_WHP_BASE_DIR
        self.whp_suffix = Config.WHP_SUFFIX

        shutil.copy(self.master_prog_path, self.res_prog_path)
        await self.vgpc.load_tool(self.res_prog_path)
        await self.vgpc.save_tool(self.res_prog_path)
        await self.vgpc.delete_all_flanges()
        return self # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        This __aexit__() method performs the following tasks:
        1) Save the file
        2) If an error occured, rename it appending "_FAILED" to the file name
        3) Close the file
        """
        await self.vgpc.save_tool(self.res_prog_path)

        if traceback is not None:
            old_name = self.res_prog_path.stem
            old_extension = self.res_prog_path.suffix
            directory = self.res_prog_path.parent
            new_name = old_name + "_FAILED" + old_extension
            self.res_prog_path.rename(Path(directory, new_name))

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
        This method return the Craete (FOR NEW PROGRAMS ONLY!!!) wheelpack full path, given its name
        """
        pthlb_whp_path = Path(self.std_whp_base_dir).joinpath(whp_name + Config.CREATE_WHP_SUFFIX + self.whp_suffix)
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
import shutil
import asyncio
from pathlib import Path
import win32com.client
import logging

from autoprogram.errors import *
from autoprogram.wbhandler import WorkBook
from autoprogram.config import Config
from autoprogram.common import try_more_times

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

class Meta(type):
    """
    Metaclass defined in order to assess that the tool classes have determined
    class variables and methods, then creates other class variables depending
    on the first ones
    """
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)
        if name != "BaseTool":
            if not "family_address" in attrs:
                raise AttributeError("Tool class without family_address class attribute.")
            if not "machine" in attrs:
                raise AttributeError("Tool class without machine class attribute.")
            if not "set_parameters" in attrs:
                raise AttributeError("Tool class without set_parameters method.")
            if not "set_wheels" in attrs:
                raise AttributeError("Tool class without set_wheels method.")
            if not "set_isoeasy" in attrs:
                raise AttributeError("Tool class without set_isoeasy method.")
            if not "set_datasheet" in attrs:
                raise AttributeError("Tool class without set_datasheet method.")
            # Create class variables depending on tool class
            cls.family_dir = Path(Config.MASTER_PROGS_BASE_DIR).joinpath(cls.family_address) # self.family_address is a child class variable (initialized in a child class of BaseTool)
            cls.master_prog_path = cls.family_dir.joinpath(Config.MASTER_PROG_DIR, Config.MASTER_PROG_NAME + "_" + cls.machine + Config.VGP_SUFFIX)
            cls.worksheets_dir = cls.family_dir.joinpath(Config.WORKSHEETS_DIR)
            cls.isoeasy_dir = cls.family_dir.joinpath(Config.ISOEASY_DIR)
            # Read common worksheet
            cls.common_wb = WorkBook(Config.COMMON_WB_PATH)
            # Read create filee
            try:
                create_wb_path = cls.worksheets_dir.joinpath(Config.CREATE_FILE_NAME)
                create_dict = WorkBook(create_wb_path).wb
                create_dict_values = [*create_dict.values()]
                cls.create_wb = create_dict_values[0]
            except ValueError:
                raise WrongCreateFileName
            # Read configuration file
            try:
                configuration_wb_path = cls.worksheets_dir.joinpath(Config.CONFIG_FILE_NAME)
                cls.configuration_wb = WorkBook(configuration_wb_path)
            except ValueError:
                raise WrongConfigurationFileName
        return cls


class BaseTool(metaclass=Meta):

    def __init__(self, vgp_client, name):
        self.vgpc = vgp_client # active VgpClient instance (whose __aenter__ method has been run)
        self.name = name
        self.whp_names_list = []
        self.datasheet_args = []

    async def __aenter__(self):
        """
        __aenter__() method:
        """
        self.complete_name = self.name + "_" + self.__class__.machine
        self.res_prog_dir = Path(Config.RES_PROGS_DIR).joinpath(self.complete_name)
        try:
            self.res_prog_dir.mkdir(parents=True)
        except FileExistsError:
            shutil.rmtree(self.res_prog_dir)
            self.res_prog_dir.mkdir(parents=True)

    
        self.res_prog_path = self.res_prog_dir.joinpath(self.complete_name + Config.VGP_SUFFIX)
        self.datasheet_path = self.res_prog_dir.joinpath("DS_" + self.complete_name + ".txt")

        shutil.copyfile(self.master_prog_path, self.res_prog_path)
        await self.load_tool(self.res_prog_path)
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
        await self.vgpc.close_file()

        if traceback is not None:
            old_name = self.res_prog_path.stem
            old_extension = self.res_prog_path.suffix
            directory = self.res_prog_path.parent
            new_name = old_name + "_FAILED" + old_extension
            self.res_prog_path.rename(Path(directory, new_name))
            res_prog_dir_failed_str = str(self.res_prog_dir)
            self.res_prog_dir.rename(res_prog_dir_failed_str)
            _logger.error(old_name + " FAILED!")

    def check_boundary(self, arg, low_bound, up_bound):
        """
        This method raises an error if the argument value is not between the
        lower and the upper boundaries
        """
        if arg < low_bound or arg > up_bound:
            self.error_list(0)

    def full_whp_path(self, whp_name):
        """
        This method return the Create (FOR NEW PROGRAMS ONLY!!!) wheelpack full path, given its name
        """
        pthlb_whp_path = Path(Config.STD_WHP_DIR).joinpath(whp_name + Config.CREATE_WHP_SUFFIX + Config.WHP_SUFFIX)
        str_whp_path = str(pthlb_whp_path)
        return str_whp_path

    def full_png_path(self, whp_name):
        """
        This method return the wheelpack PNG full path, given its name
        """
        pthlb_png_path = Path(Config.STD_PNG_DIR).joinpath(whp_name + Config.PNG_SUFFIX)
        str_png_path = str(pthlb_png_path)
        return str_png_path

    def full_isoeasy_path(self, isoeasy_name):
        """
        This method return full isoeasy path to be loaded, depending on the tool family
        """
        pthlb_isoeasy_path = Path(self.isoeasy_dir).joinpath(isoeasy_name + Config.ISOEASY_SUFFIX)
        str_isoeasy_path = str(pthlb_isoeasy_path)
        return str_isoeasy_path

    def write_datasheet(self):
        """
        This method must be used in set_datasheet method.
        It Writes arguments and wheelpack names on a text file
        """
        with open(self.datasheet_path, 'w') as f:
            # Header
            f.write(self.complete_name + " datasheet\n\n")
            # Custom arguments
            for arg in self.datasheet_args:
                f.write(arg + "\n\n")
            # Wheelpacks
            f.write("Wheelpacks:\n")
            for whp_name in self.whp_names_list:
                f.write(whp_name)

    def create_shortcut(self, source_raw_path, shortcut_raw_path):
        source_path = str(source_raw_path)
        shortcut_path = str(shortcut_raw_path)
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = source_path
        shortcut.IconLocation = source_path
        shortcut.Save()

    def create_whp_png_shortcut(self, whp_name):
        str_png_path = self.full_png_path(whp_name)
        pthlb_shorcut_path = Path(self.res_prog_dir).joinpath(whp_name + ".lnk")
        str_shorcut_path = str(pthlb_shorcut_path)
        self.create_shortcut(str_png_path, str_shorcut_path)

    @try_more_times
    async def load_tool(self, raw_path):
        await self.vgpc.load_tool(raw_path)

    async def load_wheel(self, whp_name, whp_posn):
        whp_path = self.full_whp_path(whp_name)
        await self.vgpc.load_wheel(whp_path, whp_posn)
        whp_pos_name = str(whp_posn) + ") " + (whp_name) + "\n"
        self.whp_names_list.append(whp_pos_name)
        self.create_whp_png_shortcut(whp_name)


    async def create(self):
        """
        Wrap the three methods necessary to create the tool
        """
        await self.set_parameters()
        await self.set_wheels()
        await self.set_isoeasy()
        self.set_datasheet()
        self.write_datasheet()

    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            raise ValueError("The input argument is out of boundary.")
        if err_id == 1:
            raise FileNotFoundError("Load tool max attempts exceeded.")
import shutil
import asyncio
import numpy as np
import pandas as pd
from pathlib import Path
import logging

from autoprogram.errors import *
from autoprogram.wbhandler import WorkBook
from autoprogram.dshandler import DataSheet
from autoprogram.config import Config
from autoprogram.common import try_more_times, full_pathlib_path, create_res_shortcut_from_file_name, is_nan


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


MAX_ASYNC_REQUESTS = 1
CYCLE_TIME_NODEID = "ns=2;s=ProgramMetadata/CycleTime"
CYCLE_TIME_LOG_FILE_NAME = "cycle_time_log.xlsx"
CYCLE_TIME_LOG_COLUMNS = ['name', 'simulation cycle time [s]']


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
            if not "set_wheel_segments" in attrs:
                raise AttributeError("Tool class without set_wheel_segments method.")
            if not "set_isoeasy" in attrs:
                raise AttributeError("Tool class without set_isoeasy method.")
            if not "set_datasheet" in attrs:
                raise AttributeError("Tool class without set_datasheet method.")
            # Create class variables depending on tool class
            cls.family_dir = Path(Config.MASTER_PROGS_BASE_DIR).joinpath(cls.family_address) # self.family_address is a child class variable (initialized in a child class of BaseTool)
            cls.master_prog_path = cls.family_dir.joinpath(Config.MASTER_PROG_DIR, Config.MASTER_PROG_NAME + "_" + cls.machine + Config.VGP_SUFFIX)
            cls.worksheets_dir = cls.family_dir.joinpath(Config.WORKSHEETS_DIR)
            cls.isoeasy_dir = cls.family_dir.joinpath(Config.ISOEASY_DIR)
            cls.images_dir = cls.family_dir.joinpath(Config.IMAGES_DIR)
            # Set configuration file path
            cls.create_wb_path = cls.worksheets_dir.joinpath(Config.CREATE_FILE_NAME)
            # Set configuration file path
            cls.configuration_wb_path = cls.worksheets_dir.joinpath(Config.CONFIG_FILE_NAME)
        return cls


class BaseTool(metaclass=Meta):

    def __init__(self, vgp_client, name):
        self.vgpc = vgp_client # active VgpClient instance (whose __aenter__ method has been run)
        self.name = name
        self.params_list = []
        self.whp_df = pd.DataFrame(columns=["whp_name"], index=range(1, 7))
        self.isoeasy_name = None
        self.ds_text_args = []
        self.ds_img_names = []
        self.cycle_time = None

        # Read common file
        try:
            self.common_wb = WorkBook(Config.COMMON_WB_PATH)
        except ValueError:
            raise WrongCommonFileName

        # Read configuration file
        try:
            self.configuration_wb = WorkBook(self.configuration_wb_path)
        except ValueError:
            raise WrongConfigurationFileName

    async def __aenter__(self):
        """
        __aenter__() method:
        """
        self.complete_name = self.name + "_" + self.__class__.machine
        self.res_prog_dir = Path(Config.RES_PROGS_DIR).joinpath(self.complete_name)
        self.cycle_time_log_path = Path(Config.RES_PROGS_DIR).joinpath(CYCLE_TIME_LOG_FILE_NAME)
        try:
            self.res_prog_dir.mkdir(parents=True)
        except FileExistsError:
            shutil.rmtree(self.res_prog_dir)
            self.res_prog_dir.mkdir(parents=True)

    
        self.res_prog_path = self.res_prog_dir.joinpath(self.complete_name + Config.VGP_SUFFIX)
        self.datasheet_path = self.res_prog_dir.joinpath("DS_" + self.complete_name + ".docx")

        shutil.copyfile(self.master_prog_path, self.res_prog_path)

        try:
            await self.load_tool(self.res_prog_path)
        except TryMoreTimesFailed:
            raise LoadToolFailed

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
            raise InputParameterOutOfBoundary(arg)

    @try_more_times(max_attempts=10, timeout=30, wait_period=1, retry_exception=FileNotFoundError)
    async def load_tool(self, raw_path):
        await self.vgpc.load_tool(raw_path)

    def set(self, nodeid, raw_val):
        """
        Store nodeid and raw value in a list
        """
        self.params_list.append([nodeid, raw_val])

    async def write_parameters(self):
        """
        Write asynchronously raw values in the program at the specified nodeids
        """
        params_df = pd.DataFrame(self.params_list, columns=['nodeid', 'raw_val'])
        # Divide DataFrame in chunks in order to make not too many asynchronous request
        params_df_list = [params_df[i:i + MAX_ASYNC_REQUESTS] for i in range(0, params_df.shape[0], MAX_ASYNC_REQUESTS)]
        for params_df_chunk in params_df_list:
            await asyncio.gather(*[self.vgpc.write(row[1].nodeid, row[1].raw_val) for row in params_df_chunk.iterrows()]) # row[1] because row[0] is the index

    async def get(self, nodeid):
        return await self.vgpc.read(nodeid)

    async def load_wheel(self, whp_name, whp_posn):
        """
        This method calls the opc-ua method to load a wheelpack in the selected
        position
        """
        pthlb_whp_path = full_pathlib_path(Config.STD_WHP_DIR, whp_name, Config.CREATE_WHP_SUFFIX + Config.WHP_SUFFIX)
        str_whp_path = str(pthlb_whp_path)
        await self.vgpc.load_wheel(str_whp_path, whp_posn)

    def set_wheel(self, whp_name, whp_posn):
        """
        Store wheelpack name and its position in a list
        """
        self.whp_df.loc[whp_posn] = whp_name

    def create_whp_png_shortcut(self, whp_name):
        create_res_shortcut_from_file_name(Config.STD_PNG_DIR, whp_name, Config.PNG_SUFFIX, self.res_prog_dir)

    async def load_wheels(self):
        """
        Load synchronously wheelpacks in the program
        """
        for row in self.whp_df.iterrows():
            whp_name = row[1].whp_name
            whp_posn = row[0] # row index
            # if the position is not empty, the wheelpack is loaded in the program and a shortcut is created
            if is_nan(whp_name):
                row[1].whp_name = "Empty"
            else:
                await self.load_wheel(whp_name, whp_posn)
                self.create_whp_png_shortcut(whp_name)

    async def load_isoeasy(self):
        """
        Load specified isoeasy program
        """
        if self.isoeasy_name is not None:
            str_full_isoeasy_path = str(full_pathlib_path(self.isoeasy_dir, self.isoeasy_name, Config.ISOEASY_SUFFIX))
            await self.vgpc.load_isoeasy(str_full_isoeasy_path)

    async def calculate_cycle_time(self):
        """
        Calculate cycle time and save it in an object variable
        """
        await self.vgpc.calculate_cycle_time()
        cycle_time_temp = await self.get(CYCLE_TIME_NODEID) # get cycle time in seconds
        self.cycle_time = round(cycle_time_temp)

    def write_datasheet(self):
        """
        This method must be used in set_datasheet method.
        It Writes arguments and wheelpack names on a text file
        """
        with DataSheet(self.datasheet_path) as ds:
            # Datasheet header
            ds.add_heading(self.complete_name + " Datasheet")
            # Datasheet cycle time text
            cycle_time_h = round(self.cycle_time/36, 3) # convert seconds in decimal hours
            cycle_time_text = "Cycle time: " + str(cycle_time_h) + " H"
            self.ds_text_args.append(cycle_time_text)
            # Datasheet custom text
            if self.ds_text_args is not None:
                ds.add_text_arguments(self.ds_text_args)
            # Datasheet images
            # Convert names to full paths
            if self.ds_img_names is not None:
                ds_img_paths = [full_pathlib_path(self.images_dir, img_name, Config.PNG_SUFFIX) for img_name in self.ds_img_names]
                ds.add_pictures(ds_img_paths, 80, 80)
            # Wheelpacks position and name
            ds.add_wheelpacks_table(self.whp_df)

    def write_cycle_time_log(self):
        try:
            cycle_time_log_wb = WorkBook(self.cycle_time_log_path)
            cycle_time_log_df = cycle_time_log_wb.get_first_sh_df()
        except ValueError:
            cycle_time_log_df = pd.DataFrame(columns=CYCLE_TIME_LOG_COLUMNS)

        df_concat = pd.DataFrame([[self.name, self.cycle_time]], columns=CYCLE_TIME_LOG_COLUMNS)
        cycle_time_log_df = pd.concat([cycle_time_log_df, df_concat], ignore_index=True)
        cycle_time_log_df.to_excel(self.cycle_time_log_path, index=False)

    async def create(self):
        """
        Wrap the methods necessary to create the tool
        """
        await self.set_parameters()
        await self.write_parameters()
        self.set_wheels()
        await self.load_wheels()
        self.params_list = [] # needed by set_wheel_segments to have an empty list to append to
        self.set_wheel_segments()
        await self.write_parameters()
        self.set_isoeasy()
        await self.load_isoeasy()
        await self.calculate_cycle_time()
        self.set_datasheet()
        self.write_datasheet()
        self.write_cycle_time_log()
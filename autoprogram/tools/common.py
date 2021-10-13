import re
from pathlib import Path

from autoprogram.vgpro import VgpClient
from autoprogram import config


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
        return super().__new__(cls, name, bases, body)


class BaseTool(metaclass=Meta):
    def __init__(self, vgp_client, name, family_address):
        self.name = name
        self.vgpc = vgp_client
        self.master_prog_path = Path(config.MASTER_PROGS_BASE_DIR).joinpath(family_address, config.MASTER_PROG_NAME + config.VGP_SUFFIX)
        self.res_prog_path = Path(config.RES_PROGS_DIR).joinpath(name + config.VGP_SUFFIX)

    async def __aenter__(self):
        """
        This __aenter__() method performs the following tasks:
        1) Load the correct master program
        2) Save the program on the local machine
        """
        await self.vgpc.load_tool(self.master_prog_path)
        await self.vgpc.save_tool(self.res_prog_path)
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

    # @staticmethod
    # def vgp_str_to_float(vgp_str_val):
    #     """
    #     Call the method to convert a vgp string to a float
    #     """
    #     return vgp_str_to_float(vgp_str_val)

    async def delete_all_flanges(self):
        """
        Delete all flanges in order to speed up calculations
        """
        await self.vgp.delete_all_flanges()

    async def create(self):
        """
        Wrap the three methods necessary to create the tool
        """
        # await self.delete_all_flanges()
        await self.set_parameters()
        await self.set_wheels()

    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            raise ValueError("The input argument is out of boundary.")
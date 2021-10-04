from pathlib import Path

from autoprogram.vgpprogram import VgpProgram
from autoprogram import config


class Tool:
    def __init__(self, name, family_address):
        self.name = name
        self.vgp = VgpProgram(config.SERVER_URL)
        self.master_prog_path = Path(config.MASTER_PROGS_BASE_DIR).joinpath(family_address, config.MASTER_PROG_NAME + config.VGP_SUFFIX)
        self.res_prog_path = Path(config.RES_PROGS_DIR).joinpath(name + config.VGP_SUFFIX)

    async def __aenter__(self):
        """
        Append other operations after the vgp.__aenter__method:
        1) Load the correct master program
        2) Save the program on the local machine
        """
        await self.vgp.__aenter__()
        await self.vgp.load_tool(self.master_prog_path)
        await self.vgp.save_tool(self.res_prog_path)
        return self # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Append two operations before calling the vgp.__aexit__() method
        1) Save the program
        2) Close the file
        """
        await self.vgp.save_tool(self.res_prog_path)
        await self.vgp.close_file()
        await self.vgp.__aexit__(exc_type, exc_value, traceback)

    def check_boundary(self, arg, low_bound, up_bound):
        """
        This method raises an error if the argument value is not between the
        lower and the upper boundaries
        """
        if arg < low_bound or arg > up_bound:
            self.error_list(0)

    async def delete_all_flanges(self):
        """
        Delete all flanges in order to speed up calculations
        """
        await self.vgp.delete_all_flanges()

    async def set_parameters(self):
        raise AttributeError("Tool object without set_parameters(self) method")

    async def set_wheels(self):
        raise AttributeError("Tool object without set_wheels(self) method")

    async def create(self):
        """
        Wrap the three methods necessary to create the tool
        """
        await self.delete_all_flanges()
        await self.set_parameters()
        await self.set_wheels()

    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            print("The input argument is out of boundary.")
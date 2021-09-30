from pathlib import Path

from autoprogram.vgpprogram import VgpProgram
from autoprogram import config


class Tool:
    def __init__(self, name, family_address):
        self.name = name
        self.vgp = VgpProgram(config.SERVER_URL)
        self.master_prog_path = Path(config.MASTER_PROGS_BASE_DIR).joinpath(family_address, config.MASTER_PROG_NAME).with_suffix(config.VGP_SUFFIX)
        self.res_prog_path = Path(config.RES_PROGS_DIR).joinpath(name).with_suffix(config.VGP_SUFFIX)

    async def __aenter__(self):
        """
        Append the subscription to the application state node
        after the Client __aenter__method
        """
        await self.vgp.__aenter__()
        # Load the correct master program and save on the local machine
        await self.vgp.load_tool(self.master_prog_path)
        await self.vgp.save_tool(self.res_prog_path)
        return self # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Just call the Client __aexit__ method
        """
        await self.vgp.save_tool(self.res_prog_path)
        await self.vgp.close_file()
        await self.vgp.__aexit__(exc_type, exc_value, traceback)

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
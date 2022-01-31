import subprocess
import logging
import time


# Set vgpapp logging level to INFO
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


VGPRO_EXE_PATH = "C:/Program Files (x86)/ROLLOMATIC/VirtualGrindPro/1.33.2/bin/VirtualGrindPro.exe"
R628XW_ID = "R628XW"
R628XW_ARG = "../MachinesRes/Machines/Cnc628xw/v7.0.37.0/cnc628xw.rds"


class VgpApp:
    def __init__(self, machine):
        """
        Create an instance of the VgPro class, which manages the VgPro
        application
        """
        self.machine = machine.__str__()

    def __enter__(self):
        """
        Open the VgPro application
        """
        self.start_application() # start VgPro application
        # await self.vgp_client.__aenter__() # start OPC-UA client connection
        return self # very important!!!

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the VgPro application
        """
        # await self.vgp_client.__aexit__(exc_type, exc_value, traceback) # Close the OPC-UA connection with the server
        self.close_application(exc_type, exc_value, traceback) # close the VgPro application

    def start_application(self):
        """
        Start VgPro application
        """
        if self.machine == R628XW_ID:
            mach_arg = R628XW_ARG
        else:
            self.error_list(0, self.machine)

        vgp_app_target = VGPRO_EXE_PATH + " -Machine " + mach_arg + " -SilentMode true"
        _logger.info("Starting the VgProapplication: " + vgp_app_target)
        self.p = subprocess.Popen(vgp_app_target)
        self.p.__enter__()
        _logger.info(vgp_app_target + " application started!")

    def close_application(self, exc_type, exc_value, traceback):
        """
        Close the VgPro application
        """
        _logger.info("Closing VgPro application...")
        self.p.terminate()
        self.p.__exit__(exc_type, exc_value, traceback)
        _logger.info("VgPro application closed!")

    def error_list(self, err_id, *args, **kwargs):
        """
        In case of error
        """
        if err_id == 0:
            raise ValueError(f"Selected machine doesn't exist: {args[0]}")
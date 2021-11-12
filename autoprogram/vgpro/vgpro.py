import subprocess
import time

from autoprogram.vgpro import VgpClient

VGPRO_EXE_PATH = "C:/Program Files (x86)/ROLLOMATIC/VirtualGrindPro/1.33.2/bin/VirtualGrindPro.exe"
R628XW_ARG = "../MachinesRes/Machines/Cnc628xw/v7.0.37.0/cnc628xw.rds"

class VgPro:
    def __init__(self, machine):
        """
        Create an instance of the VgPro class, which manages the VgPro
        application
        """
        self.machine = machine.__str__()
        self.vgp_client = VgpClient()

    async def __aenter__(self):
        """
        Open the VgPro application and connect to the OPC-UA server
        """
        print("Starting VgPro application...", flush=True)
        if self.machine == "628xw":
            mach_arg = R628XW_ARG
        else:
            self.error_list(0)

        self.p = subprocess.Popen(VGPRO_EXE_PATH + " -Machine mach_arg -SilentMode true")
        self.p.__enter__()
        await self.vgp_client.__aenter__()
        print("VgPro application started!", flush=True)
        return self.vgp_client # very important!!!

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Disconnect from the OPC-UA server and close the VgPro application
        """
        print("Closing VgPro application...", flush=True)
        await self.vgp_client.__aexit__(exc_type, exc_value, traceback)
        self.p.terminate()
        self.p.__exit__(exc_type, exc_value, traceback)
        print("VgPro application closed!", flush=True)

    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            raise ValueError("Select machine doesn't exist.")
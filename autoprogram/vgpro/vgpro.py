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
        self.start_application() # start VgPro application
        await self.vgp_client.__aenter__() # start OPC-UA connection
        return self.vgp_client # very important!!! This is an active vgp client, that has to be passed to the context manager

    def start_application(self):
        """
        Start VgPro application
        """
        print("Starting VgPro application...", flush=True)
        if self.machine == "628xw":
            mach_arg = R628XW_ARG
        else:
            self.error_list(0)

        self.p = subprocess.Popen(VGPRO_EXE_PATH + " -Machine mach_arg -SilentMode true")
        self.p.__enter__()
        print("VgPro application started!", flush=True)

    def close_application(self, exc_type, exc_value, traceback):
        """
        Close the VgPro application
        """
        print("Closing VgPro application...", flush=True)
        self.p.terminate()
        self.p.__exit__(exc_type, exc_value, traceback)
        print("VgPro application closed!", flush=True)

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Close the OPC-UA connection and close the VgPro application
        """
        await self.vgp_client.__aexit__(exc_type, exc_value, traceback) # Close the OPC-UA connection with the server
        self.close_application(exc_type, exc_value, traceback) # close the VgPro application

    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            raise ValueError("Selected machine doesn't exist.")
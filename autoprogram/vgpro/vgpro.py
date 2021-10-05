import subprocess
import time

R628XW_ARG = "../MachinesRes/Machines/Cnc628xw/v7.0.37.0/cnc628xw.rds"

class VgPro:
    def __init__(self, exe_path, machine):
        """
        Create an instance of the VgPro class, which manages the VgPro
        application
        """
        self.exe_path = exe_path.__str__()
        self.machine = machine.__str__()

    def __enter__(self):
        """
        Open the VgPro app
        """
        if self.machine == "628xw":
            mach_arg = R628XW_ARG
        else:
            raise self.error_list(0)

        self.p = subprocess.Popen(self.exe_path + " -Machine mach_arg -SilentMode true")
        self.p.__enter__()
        return self.p # very important!!!

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the VgPro app
        """
        self.p.terminate()
        self.p.__exit__(exc_type, exc_value, traceback)

    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            return ValueError("Select machine doesn't exist.")
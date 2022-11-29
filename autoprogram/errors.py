class AutoprogramError(Exception):
    def __init__(self, args, *kwargs):
        for arg in args:
            messagebox.showerror("Autoprogram Error", arg)

class EmergencyStop(AutoprogramError):
    """Emergency stop error"""
    pass

class TryMoreTimesFailed(AutoprogramError):
    """Could not create the tool"""
    pass

class WrongCreateFileName(AutoprogramError):
    """Wrong create file name"""
    pass

class WrongCommonFileName(AutoprogramError):
    """Wrong common file name"""
    pass

class WrongConfigurationFileName(AutoprogramError):
    """Wrong create file name"""
    pass

class WbSheetOrColumnNameError(AutoprogramError):
    pass

class InputParameterOutOfBoundary(AutoprogramError):
    def __init__(self, value):
        message = f"The value {value} is out of boundary"
        super().__init__(message)

class NoSuchAFile(AutoprogramError):
    def __init__(self, filename):
        message = f"No such a file: {filename}"
        super().__init__(message)

class RConnectError(Exception):
    pass

class LoadToolFailed(RConnectError):
    pass
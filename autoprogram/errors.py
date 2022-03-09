class AutoprogramError(Exception):
    pass

class EmergencyStop(AutoprogramError):
    """Emergency stop error"""
    pass

class TryMoreTimesFailed(AutoprogramError):
    """Could not create the tool"""
    pass

class WrongCreateFileName(AutoprogramError):
    """Wrong create file name"""
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
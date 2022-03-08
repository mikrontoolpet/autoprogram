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
    pass
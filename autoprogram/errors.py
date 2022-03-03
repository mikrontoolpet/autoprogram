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

class WrongConfigurationFileName(AutoprogramError):
    """Wrong create file name"""

class WbSheetOrColumnNameError(AutoprogramError):
    pass
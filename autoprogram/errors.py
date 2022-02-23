class EmergencyStop(BaseException):
    """Emergency stop error"""
    pass

class TryMoreTimesFailed(BaseException):
    """Could not create the tool"""
    pass
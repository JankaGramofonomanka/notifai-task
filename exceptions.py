
class DatabaseFormatError(Exception):
    """Raised when data in the database is in wrong format"""
    pass

class DataDoesNotExist(Exception):
    """Raised when the requested data is npt found in the database"""

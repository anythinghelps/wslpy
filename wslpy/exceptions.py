
from http.client import EXPECTATION_FAILED

"""wslpy exceptions."""

__all__ = (
    'INVALID_CONVERSION_TYPE',
)

class INVALID_CONVERSION_TYPE(BaseException):
    #TODO: catch this exception in TBD tests
    '''Raised when a path from windows or linux is unproperly formatted. (?)'''
    ...


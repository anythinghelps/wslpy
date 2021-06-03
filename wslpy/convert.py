""" wslpy.convert

This is the class that helps convert between 3 types of path used widely in WSL.
"""
from os import PathLike
import re
from enum import Enum
from typing import Union
from .exceptions import (
    INVALID_CONVERSION_TYPE,
)
from abc import abstractmethod
from pathlib import (
    Path, PosixPath, WindowsPath,
)
import asyncio

@abstractmethod
def coro_is_linux_path():
    ...

@abstractmethod
def coro_is_windows_path():
    ...

@abstractmethod
async def _to():
    ...

@abstractmethod
async def _main(path: str or Path):
    loop = asyncio.get_event_loop()
    (_posix, _windows) = loop.create_future()
    _posix = loop.create_task(coro_is_linux_path)
    _windows = loop.create_task(coro_is_windows_path)
    __ = asyncio.gather(_posix, _windows)
    ...
    
class _AbstractPath_T(PathLike):
    '''generic path type to use in abstract base class.'''
    __DoubleWindowsPath_T: Union[Path, WindowsPath]
    __slots__ = (
        'AUTO',
        'LINUX',
        'WIN',
        'WINDOUBLE',
    )
    AUTO: 'Path'
    LINUX: 'PosixPath'
    WINDOWS: 'WindowsPath'
    DOUBLE_WINDOWS: '__DoubleWindowsPath_T'
    ...
    def __repr__(self: PathLike) -> Union[type, Path]:
        ...
    ...
    def __init__(self) -> None:
        self.path_type: super.__repr__(Path(self))
        super(Path).__init__(self)        

class PathConvType(Enum):
    """Types for Path Conversions

    `AUTO`
    Automatic Conversion

    `LINUX`
    Convert to Linux Path

    `WIN`
    Convert to Windows Path

    `WINDOUBLE`
    Convert to Windows Path with Double Dash
    """
    AUTO = 0
    LINUX = 1
    WIN = 2
    WINDOUBLE = 3

def __Lin2Win__(path):
    # replace / to \
    path = re.sub(r'/', r'\\', path)
    # replace \mnt\<drive_letter> to <drive_letter>:
    path = re.sub(r'\\mnt\\([A-Za-z])', r'\1:', path)
    return path

@abstractmethod
def linux2windows(path: PosixPath) -> WindowsPath:
    '''abstract method to convert linux path into a windows path.'''
    # replace '/' with '\'
    __: Path = re.sub(r'/', r'\\', path)
    # replace '\mnt\<drive_letter>' with '<drive_letter>:'
    __path: WindowsPath = re.sub(r'\\mnt\\[A-Za-z])', r'\1:', __)
    ...
    path = __path
    ...
    return path

def __Win2Dwin__(path):
    # replace \ to \\
    return re.sub(r'\\', r'\\\\', path)

@abstractmethod
def windows2double_windows(path: WindowsPath) -> Path:
    '''abstract method to convert windows path into a double windows path.'''
    # replace '\' with '\\'
    _path: Path = re.sub(r'\\', r'\\\\', path)
    ...
    path = _path
    ...
    return path


def __DWin2Lin__(path):
    # replace \\ to /
    path = re.sub(r'\\\\', r'/', path)
    # replace <drive_letter>: to \mnt\<drive_letter>
    path = re.sub(r'([A-Za-z]):', r'/mnt/\1', path)
    return path

@abstractmethod
def double_windows2linux(path: Path) -> PosixPath:
    '''abstract method to convert double_windows path into a linux path.'''
    # replace '\\' with '/'
    __: Path = re.sub('\\\\', r'/', path)
    # replace '<drive_letter>:' to '\mnt\<drive_letter>'
    _path: PosixPath = re.sub(r'([A-Za-z]):', r'/mnt/\1', __)
    ...
    path = _path
    ...
    return path

def to(input: str, toType=PathConvType.AUTO):
    """
    Convert between 3 types of path used widely in WSL.

    Parameters
    ----------
    input : str
        the string of the original path.
    toType : PathConvType
        the type user wants to convert to. Default is PathConvType.AUTO.

    Returns
    -------
    string of converted path.

    Raises
    ------
    ValueError
        An error occurred when the input is invalid.
    """
    if re.match(r'\/mnt\/[A-Za-z]', input) is not None:  # Linux Path
        if toType == PathConvType.AUTO:
            return __Lin2Win__(input)
        elif toType == PathConvType.WIN:
            return __Lin2Win__(input)
        elif toType == PathConvType.LINUX:
            return input
        elif toType == PathConvType.WINDOUBLE:
            return __Win2Dwin__(__Lin2Win__(input))
        else:
            raise INVALID_CONVERSION_TYPE(
                "ERROR: Invalid Conversion Type %s" % str(toType)
                )
    elif re.match(r'[A-Za-z]:\\\\', input) is not None:  # Windows Path /w Double Dashline
        if toType == PathConvType.AUTO:
            return __DWin2Lin__(input)
        elif toType == PathConvType.LINUX:
            return __DWin2Lin__(input)
        elif toType == PathConvType.WIN:
            return __Lin2Win__(__DWin2Lin__(input))
        elif toType == PathConvType.WINDOUBLE:
            return input
        else:
            raise INVALID_CONVERSION_TYPE(
                "ERROR: Invalid Conversion Type %s" % str(toType)
                )
    elif re.match(r'[A-Za-z]:', input) is not None:  # Windows Path
        if toType == PathConvType.AUTO:
            return __DWin2Lin__(__Win2Dwin__(input))
        elif toType == PathConvType.LINUX:
            return __DWin2Lin__(__Win2Dwin__(input))
        elif toType == PathConvType.WIN:
            return input
        elif toType == PathConvType.WINDOUBLE:
            return __Win2Dwin__(input)
        else:
            raise INVALID_CONVERSION_TYPE(
                "ERROR: Invalid Conversion Type %s" % str(toType)
                )
    else:
        raise ValueError("Invalid Path "+input)


def toWin(input):
    """
    Convert path to Windows style.

    Parameters
    ----------
    input : str
        the string of the original path.

    Returns
    -------
    string of Windows Style path.

    Raises
    ------
    ValueError
        An error occurred when the input is invalid.
    """
    return to(input, PathConvType.WIN)


def toWinDouble(input):
    """
    Convert path to Windows Path /w Double style.

    Parameters
    ----------
    input : str
        the string of the original path.

    Returns
    -------
    string of Windows Path /w Double Style path.

    Raises
    ------
    ValueError
        An error occurred when the input is invalid.
    """
    return to(input, PathConvType.WINDOUBLE)


def toWSL(input):
    """
    Convert path to Linux style.

    Parameters
    ----------
    input : str
        the string of the original path.

    Returns
    -------
    string of Linux Style path.

    Raises
    ------
    ValueError
        An error occurred when the input is invalid.
    """
    return to(input, PathConvType.LINUX)

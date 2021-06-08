import typing
import os.path
import wslpy.convert as wsl_convert
import wslpy.exec as wsl_exec
import wslpy.system as wsl_system
import abc

# TODO: phase out
def isWSL():
    """
    Check whether the system is WSL.

    Returns
    -------
    A boolean value, `True` if it is WSL.
    """
    return os.path.exists('/proc/sys/fs/binfmt_misc/WSLInterop')


class _WSL_T(type):
    """Abstract Base Class for classes representing WSL-specific platform functions"""
    __name__ = 'WSL'
    __qualname__ = 'WSL_T'

    def __instancecheck__(self, instance: typing.Any) -> bool:
        ''' Check whether the instance is `WSL`. '''
        return os.path.exists('/proc/sys/fs/binfmt_misc/WSLInterop')
    
    def __repr__(self):
        return 'WSL'
    
    def __init__(self) -> None:
        super(object).__init__(self)


class WSL(_WSL_T, object):
    """Generic WSL object"""
    system: wsl_system 
    # kinda want to label 'wsl_system' -> subsystem of windows [running linux] for better abstraction.
    execution: wsl_exec
    conversion: wsl_convert

    # TODO: merge conversion typing over to wsl_module scope; get rid of convert namespace.
    @abc.abstractclassmethod
    def convert_to(cls, sys_t: typing.Optional[typing.Any['WindowsPath', 'Path', 'PosixPath', str]]) -> wsl_convert.PathLike:
        ...
        _ : cls.conversion.PathConvType = cls.conversion.toWSL # AUTO
        ...
        cls._path = _
        ...
        return cls._path

    @abc.abstractclassmethod
    def execute(cls, *args, **kwargs):
        ...
    
    @abc.abstractclassmethod
    def invoke_syscall(cls, *args, **kwargs):
        ...
    
    def __init__(self) -> None:
        """ WIP superclass """
        # self._path = '~/'
        # self.__path = ''
        super().__init__()
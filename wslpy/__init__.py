"""WSLpy module"""

import abc
import typing
import os.path

import wslpy.convert as wsl_convert
import wslpy.exec as wsl_exec
import wslpy.system as wsl_system

if typing.TYPE_CHECKING:
    from typing import Any, Optional
    from wslpy.convert import PathConvType
__all__ = ['WSL']

isWSL: bool = os.path.exists('/proc/sys/fs/binfmt_misc/WSLInterop')


class _WSL_T(type):
    """Abstract Base Class for classes representing WSL-specific platform functions"""
    __name__ = 'WSL'
    __qualname__ = 'WSL_T'

    def __instancecheck__(self, instance: Any) -> bool:
        ''' Check whether the instance is `WSL`. '''
        return isWSL
    
    def __repr__(self):
        return 'WSL'
    
    def __init__(self) -> None:
        super(object).__init__(self)


class WSL(_WSL_T, object):
    """Generic WSL object"""
    system: wsl_system 
    # Draft -- implictly cast objects by their use case behaviour
    # TODO 'wsl_system' -> subsystem of windows [running linux] for better abstraction.
    # TODO: 'win_system' => Windows || Windows :: Linux -> wsl_system
    # TODO: 'linux_subsystem' => 'WSL'
    # TODO: 'linux_system' => POSIX :: Microsoft subsystem := Windows
    # TODO: 'microsoft_subsystem'(?)
    execution: wsl_exec
    conversion: wsl_convert

    # TODO: merge conversion typing over to wsl_module scope; get rid of convert namespace.
    @abc.abstractclassmethod
    def convert_to(cls, syspath_t: Optional[PathConvType]) -> PathConvType:
        ...
        _ : PathConvType = cls.conversion.toWSL # AUTO
        ...
        cls._path = _
        ...
        if cls.__path == cls._path:
            # if the result is the same return WSL object 
            return cls
        return _

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
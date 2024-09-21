from abc import ABC, abstractmethod

from . import HasFlags

class HasSettableFlags(HasFlags, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def set_flag(self, name:str, value:bool|None) -> None:
        raise NotImplementedError
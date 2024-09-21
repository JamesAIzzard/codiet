from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from codiet.model.flags import Flag

class HasFlags(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @abstractmethod
    def get_flag(self, name: str) -> 'Flag':
        raise NotImplementedError
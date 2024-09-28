from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod

T = TypeVar('T')

class JSONToObjectFactory(Generic[T], ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @abstractmethod
    def build(self, name:str, data:Any) -> T:
        pass
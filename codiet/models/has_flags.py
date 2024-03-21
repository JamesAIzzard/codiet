from abc import ABC, abstractmethod
from typing import Dict

class HasReadableFlags(ABC):
    """A class that has flags that can be read."""
    @property
    @abstractmethod
    def flags(self) -> Dict[str, bool]:
        pass

class HasSettableFlags(HasReadableFlags):
    """A class that has flags that can be set."""
    @abstractmethod
    def set_flags(self, flags: Dict[str, bool]) -> None:
        pass
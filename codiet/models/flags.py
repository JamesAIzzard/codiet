from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.db.database_service import DatabaseService

class HasReadableFlags(ABC):
    """A class that has flags that can be read."""
    @property
    @abstractmethod
    def flags(self) -> dict[str, bool]:
        pass

class HasSettableFlags(HasReadableFlags):
    """A class that has flags that can be set."""
    @abstractmethod
    def set_flags(self, flags: dict[str, bool]) -> None:
        pass

def get_missing_flags(flags_list: list[str], db_service:'DatabaseService') -> list[str]:
    """Returns a list of flags that are missing from the flags list."""
    all_flags = db_service.fetch_flag_names()
    return [flag for flag in all_flags if flag not in flags_list]
from abc import ABC, abstractmethod

# from codiet.db.database_service import DatabaseService

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

# def missing_flags(list[str]) -> list[str]:
#     """Returns a list of flags that are missing."""
#     with database_service as db:
#         all_flags = db.fetch_flag_names()
#     return [flag for flag in all_flags if flag not in flags]
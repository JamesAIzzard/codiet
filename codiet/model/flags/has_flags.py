from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from codiet.model.flags import Flag

class HasFlags(Protocol):
    def get_flag(self, name: str) -> 'Flag':...
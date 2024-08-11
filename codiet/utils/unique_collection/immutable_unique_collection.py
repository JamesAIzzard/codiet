from typing import Iterable, TypeVar

from .base_unique_collection import BaseUniqueCollection

T = TypeVar('T')

class ImmutableUniqueCollection(BaseUniqueCollection[T]):
    def __init__(self, items: Iterable[T]|None = None):
        super().__init__(items)

    def __hash__(self):
        return hash(self._items)

    def __eq__(self, other):
        if not isinstance(other, ImmutableUniqueCollection):
            return NotImplemented
        return self._items == other._items
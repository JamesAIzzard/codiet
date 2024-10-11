from collections.abc import Mapping, ValuesView
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')

from .base_unique_dict import UniqueDictBase

class FrozenUniqueDict(UniqueDictBase[K, V], Mapping):
    def __hash__(self) -> int:
        return hash(frozenset(self._data.items()))

    def __eq__(self, other) -> bool:
        if isinstance(other, FrozenUniqueDict):
            return self._data == other._data
        return False

    def values(self) -> ValuesView[V]:
        return super().values()
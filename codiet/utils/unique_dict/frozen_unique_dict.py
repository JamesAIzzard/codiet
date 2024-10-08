from collections.abc import Mapping
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')

from .base_unique_dict import UniqueDictBase

class FrozenUniqueDict(UniqueDictBase[K, V], Mapping):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hash = None

    def __hash__(self) -> int:
        if self._hash is None:
            items = tuple(sorted(self._data.items()))
            self._hash = hash(items)
        return self._hash

    def __eq__(self, other) -> bool:
        if isinstance(other, FrozenUniqueDict):
            return self._data == other._data
        return False
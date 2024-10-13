from collections.abc import MutableMapping
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')

from .base_unique_dict import UniqueDictBase

class UniqueDict(UniqueDictBase[K, V], MutableMapping):
    def __setitem__(self, key: K, value: V) -> None:
        if value in self._data.values() and self._data.get(key) != value:
            raise ValueError(f"Value {value!r} is already in the dictionary")
        self._data[key] = value

    def __delitem__(self, key: K) -> None:
        del self._data[key]

    def clear(self) -> None:
        self._data.clear()

    def update(self, *args, **kwargs) -> None:
        new_data = dict(*args, **kwargs)
        for key, value in new_data.items():
            self[key] = value

    def copy(self) -> 'UniqueDict[K, V]':
        return UniqueDict(self._data.copy())            
from collections.abc import MutableMapping
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')

from .base_unique_dict import UniqueDictBase
from .utils import check_values_are_unique

class UniqueDict(UniqueDictBase[K, V], MutableMapping):
    def __setitem__(self, key: K, value: V) -> None:
        if key in self._data:
            old_value = self._data[key]
            if old_value == value:
                return
            self._values_set.discard(old_value)
        if value in self._values_set:
            raise ValueError(f"Value {value!r} is already in the dictionary")
        self._data[key] = value
        self._values_set.add(value)

    def __delitem__(self, key: K) -> None:
        value = self._data.pop(key)
        self._values_set.discard(value)

    def update(self, *args, **kwargs) -> None:
        items = dict(*args, **kwargs)
        check_values_are_unique(items)
        for key, value in items.items():
            self[key] = value

    def clear(self) -> None:
        self._data.clear()
        self._values_set.clear()
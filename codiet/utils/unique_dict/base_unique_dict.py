from typing import TypeVar, Generic, Iterator

from .utils import check_values_are_unique

K = TypeVar('K')
V = TypeVar('V')

class UniqueDictBase(Generic[K, V]):
    def __init__(self, *args, **kwargs):
        items = dict(*args, **kwargs)
        check_values_are_unique(items)
        self._data: dict[K, V] = items
        self._values_set = set(items.values())

    def __contains__(self, key: K) -> bool:
        return key in self._data

    def __getitem__(self, key: K) -> V:
        return self._data[key]

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data})"

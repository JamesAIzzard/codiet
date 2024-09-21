from typing import TypeVar, Generic, Iterator, Dict

K = TypeVar('K')
V = TypeVar('V')

class BaseUniqueDict(Generic[K, V]):
    def __init__(self, *args, **kwargs):
        items = dict(*args, **kwargs)
        if len(set(items.values())) != len(items.values()):
            raise ValueError("Values must be unique")
        self._data: Dict[K, V] = items
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

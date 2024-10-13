from typing import TypeVar, Generic, Iterator

K = TypeVar('K')
V = TypeVar('V')

class UniqueDictBase(Generic[K, V]):
    def __init__(self, *args, **kwargs):
        self._data: dict[K, V] = dict(*args, **kwargs)
        if len(self._data) != len(set(self._data.values())):
            raise ValueError("Values must be unique")

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

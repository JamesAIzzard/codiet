from abc import ABC
from typing import TypeVar, Iterable, Generic

T = TypeVar('T')

class BaseUniqueCollection(ABC, Generic[T]):
    def __init__(self, items: Iterable[T]|None = None):
        self._items: list[T] = []
        if items:
            for item in items:
                self._add(item)

    def _add(self, item: T) -> None:
        if item in self._items:
            raise ValueError(f"Item {item} already exists in the collection.")
        self._items.append(item)

    def _clear(self) -> None:
        self._items.clear()

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def __getitem__(self, index: int) -> T:
        return self._items[index]
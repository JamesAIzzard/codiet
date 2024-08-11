from typing import TypeVar, Iterable

from .base_unique_collection import BaseUniqueCollection

T = TypeVar('T')

class MutableUniqueCollection(BaseUniqueCollection[T]):
    def add(self, items: T|Iterable[T]) -> None:
        if isinstance(items, Iterable) and not isinstance(items, str):
            for item in items:
                self._add(item)
        else:
            self._add(items)

    def remove(self, items: T|Iterable[T]) -> None:
        if isinstance(items, Iterable) and not isinstance(items, str):
            for item in items:
                self._items.remove(item)
        else:
            self._items.remove(items)

    def update(self, items: T|Iterable[T]) -> None:
        if isinstance(items, Iterable) and not isinstance(items, str):
            for item in items:
                if item in self._items:
                    index = self._items.index(item)
                    self._items[index] = item
                else:
                    raise ValueError(f"Item {item} does not exist in the collection.")
        else:
            if items in self._items:
                index = self._items.index(items)
                self._items[index] = items
            else:
                raise ValueError(f"Item {items} does not exist in the collection.")
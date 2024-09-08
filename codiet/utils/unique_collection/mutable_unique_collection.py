from typing import TypeVar, Iterable

from .base_unique_collection import BaseUniqueCollection
from .immutable_unique_collection import ImmutableUniqueCollection

T = TypeVar('T')

class MutableUniqueCollection(BaseUniqueCollection[T]):
    """A mutable collection of unique items.
    Provides an ordered, mutable, unique collection. While sets are mutable and
    unique, they are not ordered.
    """

    @property
    def immutable(self) -> ImmutableUniqueCollection[T]:
        return ImmutableUniqueCollection(self._items)

    def add(self, items: T|Iterable[T]) -> None:
        if isinstance(items, Iterable) and not isinstance(items, str):
            for item in items:
                self._add(item)
        else:
            self._add(items) # type: ignore

    def remove(self, items: T|Iterable[T]) -> None:
        if isinstance(items, Iterable) and not isinstance(items, str):
            for item in items:
                self._items.remove(item)
        else:
            self._items.remove(items) # type: ignore

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
                index = self._items.index(items) # type: ignore
                self._items[index] = items # type: ignore
            else:
                raise ValueError(f"Item {items} does not exist in the collection.")
            
    def clear(self) -> None:
        self._clear()
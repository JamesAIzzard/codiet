from typing import Generic, TypeVar, Iterable, Iterator, List, Tuple, overload
from collections import OrderedDict

T = TypeVar('T')

class UniqueList(Generic[T]):
    def __init__(self, items: T | Iterable[T] | None = None):
        self._items: OrderedDict[T, None] = OrderedDict()
        if items is not None:
            self.add(items)

    def add(self, items: T|Iterable[T]) -> None:
        """Add an item or items to the list.
        Raises:
            ValueError: If the item is already in the list.
        """
        if isinstance(items, Iterable) and not isinstance(items, str):
            for item in items:
                self._add_single(item)
        else:
            self._add_single(items) # type: ignore

    def remove(self, items: T|Iterable[T]) -> None:
        if isinstance(items, Iterable) and not isinstance(items, str):
            for item in items:
                self._remove_single(item)
        else:
            self._remove_single(items) # type: ignore

    def update(self, items: T|Iterable[T]) -> None:
        if isinstance(items, Iterable) and not isinstance(items, str):
            for item in items:
                self._update_single(item)
        else:
            self._update_single(items) # type: ignore

    def freeze(self) -> Tuple[T, ...]:
        return tuple(self._items.keys())

    def _update_single(self, item:T) -> None:
        if item not in self._items:
            raise ValueError(f"{item} not in list")
        self._items[item] = None

    def _add_single(self, item: T) -> None:
        if item in self._items:
            raise ValueError(f"{item} already in list")
        self._items[item] = None

    def _remove_single(self, item: T) -> None:
        try:
            del self._items[item]
        except KeyError:
            raise ValueError(f"{item} not in list")

    def __len__(self) -> int:
        return len(self._items)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> List[T]: ...

    def __getitem__(self, index: int | slice) -> T | List[T]:
        keys = list(self._items.keys())
        if isinstance(index, int):
            return keys[index]
        elif isinstance(index, slice):
            return keys[index]
        else:
            raise TypeError("Index must be int or slice")

    def __iter__(self) -> Iterator[T]:
        return iter(self._items.keys())

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def __repr__(self) -> str:
        return f"UniqueList({list(self._items.keys())})"
from typing import TypeVar, Generic, Hashable

K = TypeVar('K', bound=Hashable)
V = TypeVar('V', bound=Hashable)

class BidirectionalMap(Generic[K, V]):
    """A bidirectional map that stores mappings between two types of hashable objects."""
    
    def __init__(self, one_to_one: bool = False):
        self.forward: dict[K, list[V]] = {}
        self.reverse: dict[V, list[K]] = {}
        self.one_to_one = one_to_one

    @property
    def keys(self) -> list[K]:
        """Return a list of keys from the forward mapping."""
        return list(self.forward.keys())
    
    @property
    def values(self) -> list[V]:
        """Return a list of keys from the reverse mapping."""
        return list(self.reverse.keys())

    def add_mapping(self, key: K, value: V) -> None:
        """Add a new mapping between a key and a value."""
        if self.one_to_one:
            if key in self.forward or value in self.reverse:
                raise ValueError("Cannot add mapping: key or value already exists in one-to-one map.")
            self.forward[key] = [value]
            self.reverse[value] = [key]
        else:
            if key not in self.forward:
                self.forward[key] = []
            if value not in self.reverse:
                self.reverse[value] = []
            
            self.forward[key].append(value)
            self.reverse[value].append(key)

    def remove_mapping(self, key: K, value: V) -> None:
        """Remove a specific mapping between a key and a value."""
        if key in self.forward and value in self.forward[key]:
            self.forward[key].remove(value)
            if not self.forward[key]:
                del self.forward[key]
        
        if value in self.reverse and key in self.reverse[value]:
            self.reverse[value].remove(key)
            if not self.reverse[value]:
                del self.reverse[value]

    def remove_key(self, key: K) -> None:
        """Remove all mappings for a given key."""
        if key in self.forward:
            for value in self.forward[key]:
                self.reverse[value].remove(key)
                if not self.reverse[value]:
                    del self.reverse[value]
            del self.forward[key]

    def remove_value(self, value: V) -> None:
        """Remove all mappings for a given value."""
        if value in self.reverse:
            for key in self.reverse[value]:
                self.forward[key].remove(value)
                if not self.forward[key]:
                    del self.forward[key]
            del self.reverse[value]

    def get_values(self, key: K) -> list[V]|None:
        """Return the list of values for a given key, or None if not found."""
        return self.forward.get(key)

    def get_keys(self, value: V) -> list[K]|None:
        """Return the list of keys for a given value, or None if not found."""
        return self.reverse.get(value)

    def __str__(self) -> str:
        return f"BidirectionalMap(one_to_one={self.one_to_one}, forward={self.forward}, reverse={self.reverse})"
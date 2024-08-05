from typing import TypeVar, Generic, Hashable

K = TypeVar('K', bound=Hashable)
V = TypeVar('V', bound=Hashable)

class Map(Generic[K, V]):
    """A bidirectional map that stores mappings between two types of hashable objects."""
    
    def __init__(
            self,
            from_list: list[K]|None = None,
            to_list: list[V]|None = None,
            one_to_one: bool = True
        ):
        # Raise an exception if the lists are present not the same length
        if from_list is not None and to_list is not None and len(from_list) != len(to_list):
            raise ValueError("The from_list and to_list must be the same length.")
        
        # Store whether the map is one-to-one
        self.one_to_one = one_to_one

        # Create the forward and reverse mappings
        self.forward: dict[K, list[V]] = {}
        self.reverse: dict[V, list[K]] = {}

        # If arguments were provided, add the mappings
        if from_list is not None and to_list is not None:
            assert from_list is not None
            assert to_list is not None
            if from_list is not None:
                for from_item, to_item in zip(from_list, to_list):
                    self.add_mapping(from_item, to_item)

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

    def get_values(self, key: K) -> list[V]:
        """Return the list of values for a given key. Returns an empty list if the key is not found."""
        return self.forward.get(key, [])

    def get_keys(self, value: V) -> list[K]:
        """Return the list of keys for a given value. Returns an empty list if the value is not found."""
        return self.reverse.get(value, [])

    def get_value(self, key: K) -> V:
        """
        Return a single value for a given key.
        Returns None if the key is not found.
        Raises ValueError if there is more than one value for the key.
        """
        values = self.get_values(key)
        if len(values) > 1:
            raise ValueError(f"Multiple values found for key '{key}'. Use get_values() instead.")
        if len(values) == 0:
            raise ValueError(f"No values found for key '{key}'.")
        return values[0]

    def get_key(self, value: V) -> K:
        """
        Return a single key for a given value.
        Returns None if the value is not found.
        Raises ValueError if there is more than one key for the value.
        """
        keys = self.get_keys(value)
        if len(keys) > 1:
            raise ValueError(f"Multiple keys found for value '{value}'. Use get_keys() instead.")
        if len(keys) == 0:
            raise ValueError(f"No keys found for value '{value}'.")
        return keys[0]

    def clear(self) -> None:
        """Clear all mappings."""
        self.forward.clear()
        self.reverse.clear()

    def __getitem__(self, key: K) -> V | tuple[V, ...]:
        """
        Implement the [] operator for getting values.
        Returns a single value if the key is found.
        Returns a tuple of values if the key has multiple values.
        Raises KeyError if the key is not found.
        """
        values = self.get_values(key)
        if not values:
            raise KeyError(key)
        if len(values) == 1:
            return values[0]
        else:
            return tuple(values)

    def __setitem__(self, key: K, value: V | tuple[V, ...]) -> None:
        """
        Implement the [] operator for setting values.
        Accepts either a single value or a tuple of values.
        """
        if key in self.forward:
            self.remove_key(key)
        
        if isinstance(value, tuple):
            for v in value:
                self.add_mapping(key, v)
        else:
            self.add_mapping(key, value)

    def __delitem__(self, key: K) -> None:
        """
        Implement the del operator for removing mappings.
        Removes both the key and its associated value(s) from forward and reverse mappings.
        """
        if key not in self.forward:
            raise KeyError(key)
        
        values = self.forward[key]
        del self.forward[key]
        
        for value in values:
            self.reverse[value].remove(key)
            if not self.reverse[value]:
                del self.reverse[value]

    def __contains__(self, key: K) -> bool:
        """Implement the 'in' operator for checking if a key exists."""
        return key in self.forward

    def __len__(self) -> int:
        """Return the number of mappings in the forward direction."""
        return len(self.forward)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Map):
            return NotImplemented
        return self.forward == other.forward
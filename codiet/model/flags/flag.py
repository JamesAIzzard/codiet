"""Defines the Flag class."""

from codiet.db.stored_entity import StoredEntity

class Flag(StoredEntity):

    def __init__(
            self, 
            name: str,
            value: bool|None = None,
            *args, **kwargs
        ):
        """Initialise the flag."""
        super().__init__(*args, **kwargs)

        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> bool|None:
        return self._value

    @value.setter
    def value(self, value: bool|None) -> None:
        self._value = value

    def set_value(self, value: bool|None) -> 'Flag':
        self._value = value
        return self

    def __eq__(self, other) -> bool:
        # If the other object is not a flag, they are not equal
        if not isinstance(other, Flag):
            return False
        
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return self.name
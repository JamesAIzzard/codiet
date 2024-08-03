from codiet.db.stored_entity import StoredEntity

class Flag(StoredEntity):
    """Models a flag."""

    def __init__(
            self, 
            flag_name: str, 
            flag_value:bool|None=None, 
            *args, **kwargs
        ):
        """Initialise the flag."""
        super().__init__(*args, **kwargs)

        self._flag_name = flag_name
        self._flag_value:bool = False if flag_value is None else flag_value

    @property
    def flag_name(self) -> str:
        """Get the name of the flag."""
        return self._flag_name

    @property
    def flag_value(self) -> bool:
        """Get the value of the flag."""
        return self._flag_value
    
    @flag_value.setter
    def flag_value(self, value: bool):
        """Set the value of the flag."""
        self._flag_value = value

    def __eq__(self, other) -> bool:
        """Check if two flags are equal."""
        return self.flag_name == other.flag_name
    
    def __hash__(self) -> int:
        """Return the hash of the flag name."""
        return hash(self.flag_name)
    
    def __str__(self) -> str:
        """Return the flag name."""
        return self.flag_name
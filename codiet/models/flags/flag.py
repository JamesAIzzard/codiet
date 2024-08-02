from codiet.db.stored_entity import StoredEntity

class Flag(StoredEntity):
    """Models a flag."""

    def __init__(self, flag_name: str, flag_value:bool|None=None, *args, **kwargs):
        """Initialise the flag.
        Args:
            name (str): The name of the flag.
        """
        super().__init__(*args, **kwargs)
        self._flag_name = flag_name
        self._flag_value:bool = False if flag_value is None else flag_value

    @property
    def flag_name(self) -> str:
        """Get the name of the flag."""
        return self._flag_name
    
    @flag_name.setter
    def flag_name(self, name: str):
        """Set the name of the flag."""
        # Disallow empty strings
        if not name:
            raise ValueError("Flag name cannot be empty.")
        
        self._flag_name = name

    @property
    def flag_value(self) -> bool:
        """Get the value of the flag."""
        return self._flag_value
    
    @flag_value.setter
    def flag_value(self, value: bool):
        """Set the value of the flag."""
        self._flag_value = value
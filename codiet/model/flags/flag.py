"""Defines the Flag class."""

from codiet.db.stored_entity import StoredEntity

class Flag(StoredEntity):
    """Models a flag.
    Note:
        A flag alone does not have a value. A flag only gets a value
        when it is associated with an ingredient.
    """

    def __init__(
            self, 
            flag_name: str,
            *args, **kwargs
        ):
        """Initialise the flag."""
        super().__init__(*args, **kwargs)

        self._flag_name = flag_name

    @property
    def flag_name(self) -> str:
        """Get the name of the flag."""
        return self._flag_name

    def __eq__(self, other) -> bool:
        """Check if two flags are equal."""
        return self.flag_name == other.flag_name
    
    def __hash__(self) -> int:
        """Return the hash of the flag name."""
        return hash(self.flag_name)
    
    def __str__(self) -> str:
        """Return the flag name."""
        return self.flag_name
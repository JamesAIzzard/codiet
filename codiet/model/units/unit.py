from typing import Collection

from codiet.db.stored_entity import StoredEntity

class Unit(StoredEntity):
    """Models a measurement unit."""

    def __init__(
        self,
        unit_name: str,
        single_display_name: str,
        plural_display_name: str,
        type: str,
        aliases: Collection[str]|None = None,
        *args, **kwargs
    ):
        """Initialise the unit."""
        super().__init__(*args, **kwargs)
        self._unit_name = unit_name
        self._single_display_name = single_display_name
        self._plural_display_name = plural_display_name
        self._type = type
        
        # Check any aliases provided are unique
        if aliases is not None:
            if len(aliases) != len(set(aliases)):
                raise ValueError("The aliases must be unique.")
        self._aliases = aliases or []

    @property
    def name(self) -> str:
        """Return the unit name."""
        return self._unit_name

    @property
    def single_display_name(self) -> str:
        """Return the single display name of the unit."""
        return self._single_display_name

    @property
    def plural_display_name(self) -> str:
        """Return the plural display name of the unit."""
        return self._plural_display_name
    
    @property
    def type(self) -> str:
        """Return the type of the unit."""
        return self._type

    @property
    def aliases(self) -> frozenset[str]:
        """Return the aliases of the unit."""
        return frozenset(self._aliases)
            
    def __eq__(self, other):
        """Check if two units are equal based on their unit name and type."""
        if isinstance(other, Unit):
            return self.name == other.name and self.type == other.type
        return False

    def __hash__(self):
        """Return the hash based on the unit name and type."""
        return hash((self.name, self.type))            
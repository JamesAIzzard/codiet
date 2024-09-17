from typing import Collection

from codiet.db.stored_entity import StoredEntity
from codiet.utils import MUC, IUC

class Unit(StoredEntity):
    """Models a measurement unit."""

    def __init__(
        self,
        name: str,
        type: str,
        singular_abbreviation: str|None = None,
        plural_abbreviation: str|None = None,
        aliases: Collection[str]|None = None,
        *args, **kwargs
    ):
        """Initialise the unit."""
        super().__init__(*args, **kwargs)
        self._unit_name = name
        self._type = type
        
        self._singular_abbreviation = singular_abbreviation or name
        self._plural_abbreviation = plural_abbreviation or name

        self._aliases = MUC(aliases) or MUC[str]()

    @property
    def name(self) -> str:
        """Return the unit name."""
        return self._unit_name

    @property
    def type(self) -> str:
        """Return the type of the unit."""
        return self._type

    @property
    def singular_abbreviation(self) -> str:
        """Return the single display name of the unit."""
        return self._singular_abbreviation

    @property
    def plural_abbreviation(self) -> str:
        """Return the plural display name of the unit."""
        return self._plural_abbreviation

    @property
    def aliases(self) -> IUC[str]:
        """Return the aliases of the unit."""
        return IUC(self._aliases)
            
    def __eq__(self, other):
        """Check if two units are equal based on their unit name and type."""
        if not isinstance(other, Unit):
            return False
        return self.name == other.name and self.type == other.type

    def __hash__(self):
        """Return the hash based on the unit name and type."""
        return hash((self.name, self.type))            
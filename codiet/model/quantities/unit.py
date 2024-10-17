from typing import Collection, TypedDict
from enum import Enum

from codiet.utils import MUC, IUC

class UnitType(Enum):
    MASS = "mass"
    VOLUME = "volume"
    COUNT = "count"

class UnitDTO(TypedDict):
    name: str
    type: str
    singular_abbreviation: str
    plural_abbreviation: str
    aliases: Collection[str]

class Unit:

    def __init__(
        self,
        name: str,
        type: UnitType,
        singular_abbreviation: str|None = None,
        plural_abbreviation: str|None = None,
        aliases: Collection[str]|None = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._unit_name = name
        self._type = type
        
        self._singular_abbreviation = singular_abbreviation or name
        self._plural_abbreviation = plural_abbreviation or name

        self._aliases = MUC(aliases) or MUC[str]()

    @property
    def name(self) -> str:
        return self._unit_name

    @property
    def type(self) -> UnitType:
        return self._type

    @property
    def singular_abbreviation(self) -> str:
        return self._singular_abbreviation

    @property
    def plural_abbreviation(self) -> str:
        return self._plural_abbreviation

    @property
    def aliases(self) -> IUC[str]:
        return IUC(self._aliases)
            
    def __eq__(self, other):
        if not isinstance(other, Unit):
            return False
        return self.name == other.name and self.type == other.type

    def __hash__(self):
        return hash((self.name, self.type))            
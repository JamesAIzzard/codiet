from typing import Collection, TypedDict

from codiet.model.stored_entity import StoredEntity
from codiet.utils import MUC, IUC

class UnitDTO(TypedDict):
    name: str
    type: str
    singular_abbreviation: str
    plural_abbreviation: str
    aliases: Collection[str]

class Unit(StoredEntity):

    def __init__(
        self,
        name: str,
        type: str,
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

    @classmethod
    def from_dto(cls, dto: UnitDTO) -> 'Unit':
        return cls(
            name=dto["name"],
            type=dto["type"],
            singular_abbreviation=dto["singular_abbreviation"],
            plural_abbreviation=dto["plural_abbreviation"],
            aliases=dto["aliases"],
        )

    @property
    def name(self) -> str:
        return self._unit_name

    @property
    def type(self) -> str:
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
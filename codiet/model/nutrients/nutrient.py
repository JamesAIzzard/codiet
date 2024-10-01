from typing import Collection, TypedDict

from codiet.utils.unique_dict import FrozenUniqueDict
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.model.stored_entity import StoredEntity

class NutrientDTO(TypedDict):
    name: str
    aliases: Collection[str]
    parent_name: str|None
    child_names: Collection[str]

class Nutrient(StoredEntity):

    def __init__(
        self,
        name: str,
        aliases: Collection[str]|None = None,
        parent_name: str | None = None,
        child_names: Collection[str] | None = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._name = name

        self._aliases = MUC(aliases) or MUC()
        self._parent_name = parent_name
        self._parent: 'Nutrient | None' = None
        self._child_names = MUC(child_names) or MUC()
        self._children = FrozenUniqueDict[str, 'Nutrient']()

    @classmethod
    def from_dto(cls, dto: NutrientDTO) -> 'Nutrient':
        return cls(
            name=dto['name'],
            aliases=dto['aliases'],
            parent_name=dto['parent_name'],
            child_names=dto['child_names']
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def aliases(self) -> IUC[str]:
        return IUC(self._aliases)

    @property
    def parent_name(self) -> str | None:
        return self._parent_name

    @property
    def parent(self) -> 'Nutrient':
        if not self.is_child:
            raise ValueError(f"{self.name} is not a child nutrient")
        else:
            from codiet.data import DatabaseService
            self._parent = DatabaseService().read_nutrient(self.parent_name) # type: ignore
            return self._parent
        
    @property
    def child_names(self) -> IUC[str]:
        return self._child_names.immutable

    @property
    def children(self) -> FrozenUniqueDict[str, 'Nutrient']:
        if not self.is_parent:
            return FrozenUniqueDict()
        else:
            from codiet.data import DatabaseService
            self._children = FrozenUniqueDict({child_name: DatabaseService().read_nutrient(child_name) for child_name in self.child_names})
            return self._children

    @property
    def is_parent(self) -> bool:
        return len(self.child_names) > 0
    
    @property
    def is_child(self) -> bool:
        return self.parent_name is not None

    def is_parent_of(self, nutrient_name:str) -> bool:
        if nutrient_name in self.child_names:
            return True
        for child in self.children.values():
            if child.is_parent_of(nutrient_name):
                return True
        return False
    
    def is_child_of(self, nutrient: 'Nutrient') -> bool:
        if self.parent == nutrient:
            return True
        if self.parent is not None:
            return self.parent.is_child_of(nutrient)
        return False

    def __eq__(self, other):
        if isinstance(other, Nutrient):
            return self.id == other.id and self.name == other.name
        return False

    def __hash__(self):
        return hash((self.id, self.name))
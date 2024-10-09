from typing import Collection, TypedDict

from codiet.utils.unique_dict import FrozenUniqueDict
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.model.stored_entity import StoredEntity


class NutrientDTO(TypedDict):
    name: str
    cals_per_gram: float
    aliases: Collection[str]
    parent_name: str | None
    child_names: Collection[str]


class Nutrient(StoredEntity):

    def __init__(
        self,
        name: str,
        cals_per_gram: float,        
        aliases: Collection[str] | None = None,
        parent: "Nutrient|None" = None,
        children: dict[str, "Nutrient"] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._name = name
        self._cals_per_gram = cals_per_gram
        self._aliases = MUC(aliases) or MUC()
        self._parent = parent
        self._children = (
            FrozenUniqueDict(children) or FrozenUniqueDict[str, "Nutrient"]()
        )

    @property
    def name(self) -> str:
        return self._name

    @property
    def aliases(self) -> IUC[str]:
        return IUC(self._aliases)

    @property
    def parent(self) -> "Nutrient|None":
        return self._parent

    @property
    def children(self) -> FrozenUniqueDict[str, "Nutrient"]:
        return self._children

    @property
    def is_parent(self) -> bool:
        return len(self.children) > 0

    @property
    def is_child(self) -> bool:
        return self.parent is not None

    def is_parent_of(self, nutrient_name: str) -> bool:
        if nutrient_name in self.children.keys():
            return True
        for child in self.children.values():
            if child.is_parent_of(nutrient_name):
                return True
        return False

    def is_child_of(self, nutrient: "Nutrient") -> bool:
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

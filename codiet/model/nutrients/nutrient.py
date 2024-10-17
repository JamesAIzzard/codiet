from typing import Collection, Mapping, Optional, TypedDict

from codiet.utils.unique_dict import FrozenUniqueDict
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.model.stored_entity import StoredEntity


class NutrientDTO(TypedDict):
    name: str
    cals_per_gram: float
    aliases: Collection[str]
    direct_parent_name: Optional[str]
    direct_child_names: Collection[str]


class Nutrient(StoredEntity):
    def __init__(
        self,
        name: str,
        calories_per_gram: float,
        aliases: Optional[Collection[str]] = None,
        direct_parent: Optional["Nutrient"] = None,
        direct_children: Optional[Mapping[str, "Nutrient"]] = None, # REFACTOR: Update to remove none, could just pass empty list
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._name = name
        self._calories_per_gram = calories_per_gram
        self._aliases = MUC(aliases if aliases is not None else [])
        self._direct_parent = direct_parent
        self._direct_children = FrozenUniqueDict(direct_children if direct_children is not None else {})

    @property
    def name(self) -> str:
        return self._name

    @property
    def calories_per_gram(self) -> float:
        return self._calories_per_gram

    @property
    def aliases(self) -> IUC[str]:
        return IUC(self._aliases)

    @property
    def is_child(self) -> bool:
        return self._direct_parent is not None

    @property
    def direct_parent(self) -> "Nutrient":
        if not self.is_child:
            raise ValueError(f"{self.name} has no parent nutrient.")
        return self._direct_parent  # type: ignore

    @property
    def direct_parent_name(self) -> str:
        return self.direct_parent.name

    @property
    def direct_children(self) -> FrozenUniqueDict[str, "Nutrient"]:
        return self._direct_children

    @property
    def direct_child_names(self) -> IUC[str]:
        return IUC(self.direct_children.keys())

    @property
    def is_parent(self) -> bool:
        return bool(self.direct_children)

    def is_parent_of(self, nutrient_name: str) -> bool:
        if nutrient_name in self.direct_children:
            return True
        return any(child.is_parent_of(nutrient_name) for child in self.direct_children.values())

    def is_child_of(self, nutrient_name: str) -> bool:
        if self.is_child and self.direct_parent.name == nutrient_name:
            return True
        return self.direct_parent.is_child_of(nutrient_name) if self.is_child else False

    def __eq__(self, other):
        return isinstance(other, Nutrient) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

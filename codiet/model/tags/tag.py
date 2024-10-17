from typing import TypedDict, Mapping

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.utils.unique_dict import UniqueDict as UD
from codiet.utils.unique_dict import FrozenUniqueDict as FUD

class TagDTO(TypedDict):
    name: str
    direct_parents: list[str]
    direct_children: list[str]


class Tag:

    def __init__(
        self,
        name: str,
        direct_parents: Mapping[str, "Tag"],
        direct_children: Mapping[str, "Tag"],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._name: str = name
        self._direct_parents = UD[str, "Tag"](direct_parents)
        self._direct_children = UD[str, "Tag"](direct_children)

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_child(self) -> bool:
        return len(self._direct_parents) > 0

    @property
    def is_parent(self) -> bool:
        return len(self._direct_children) > 0

    @property
    def direct_parents(self) -> FUD[str, "Tag"]:
        return self._direct_parents.immutable      

    @property
    def direct_children(self) -> FUD[str, "Tag"]:
        return self._direct_children.immutable

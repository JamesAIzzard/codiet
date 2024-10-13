from typing import TYPE_CHECKING, Collection, TypedDict, Callable
from codiet.utils.unique_collection import MutableUniqueCollection as MUC

if TYPE_CHECKING:
    from codiet.model.flags import Flag


class FlagDefinitionDTO(TypedDict):
    flag_name: str
    if_true_must_contain: Collection[str]
    if_true_cannot_contain: Collection[str]
    if_true_implies_true: Collection[str]
    if_true_implies_false: Collection[str]
    if_false_must_contain: Collection[str]
    if_false_cannot_contain: Collection[str]
    if_false_implies_true: Collection[str]
    if_false_implies_false: Collection[str]


class FlagDefinition:
    def __init__(
        self,
        flag_name: str,
        if_true_must_contain: Collection[str] | None = None,
        if_true_cannot_contain: Collection[str] | None = None,
        if_true_implies_true: Collection[str] | None = None,
        if_true_implies_false: Collection[str] | None = None,
        if_false_must_contain: Collection[str] | None = None,
        if_false_cannot_contain: Collection[str] | None = None,
        if_false_implies_true: Collection[str] | None = None,
        if_false_implies_false: Collection[str] | None = None,
    ) -> None:
        self._flag_name = flag_name
        self.if_true_must_contain = if_true_must_contain or []
        self.if_true_cannot_contain = if_true_cannot_contain or []
        self.if_true_implies_true = if_true_implies_true or []
        self.if_true_implies_false = if_true_implies_false or []
        self.if_false_must_contain = if_false_must_contain or []
        self.if_false_cannot_contain = if_false_cannot_contain or []
        self.if_false_implies_true = if_false_implies_true or []
        self.if_false_implies_false = if_false_implies_false or []

    @property
    def flag_name(self) -> str:
        return self._flag_name

    def get_names_implied_true(
        self, self_value: bool, is_nutrient_present: Callable[[str], bool]
    ) -> Collection[str]:
        implied_true = set()
        if self_value is True:
            implied_true.update(self.if_true_implies_true)
        elif self_value is False:
            implied_true.update(self.if_false_implies_true)
        
        return implied_true

    def get_names_implied_false(
        self, self_value: bool, is_nutrient_present: Callable[[str], bool]
    ) -> Collection[str]:
        implied_false = set()
        if self_value is True:
            implied_false.update(self.if_true_implies_false)
        elif self_value is False:
            implied_false.update(self.if_false_implies_false)
        
        return implied_false

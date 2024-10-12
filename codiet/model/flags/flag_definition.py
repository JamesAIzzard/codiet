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
        self._rules = {
            True: self._create_rule_set(if_true_must_contain, if_true_cannot_contain, if_true_implies_true, if_true_implies_false),
            False: self._create_rule_set(if_false_must_contain, if_false_cannot_contain, if_false_implies_true, if_false_implies_false)
        }

    @property
    def flag_name(self) -> str:
        return self._flag_name

    def get_names_implied_true(self, self_value: bool, is_nutrient_present: Callable[[str], bool]) -> Collection[str]:
        return self._get_implied_flags(self_value, is_nutrient_present, 'implies_true')

    def get_names_implied_false(self, self_value: bool, is_nutrient_present: Callable[[str], bool]) -> Collection[str]:
        return self._get_implied_flags(self_value, is_nutrient_present, 'implies_false')

    def _get_implied_flags(self, self_value: bool, is_nutrient_present: Callable[[str], bool], implication_type: str) -> Collection[str]:
        rule_set = self._rules[self_value]
        if self._nutrient_conditions_met(rule_set, is_nutrient_present):
            return rule_set[implication_type]
        return MUC[str]()

    def _nutrient_conditions_met(self, rule_set: dict, is_nutrient_present: Callable[[str], bool]) -> bool:
        return all(is_nutrient_present(nutrient) for nutrient in rule_set['must_contain']) and \
               all(not is_nutrient_present(nutrient) for nutrient in rule_set['cannot_contain'])

    @staticmethod
    def _create_rule_set(must_contain, cannot_contain, implies_true, implies_false):
        return {
            'must_contain': MUC(must_contain or []),
            'cannot_contain': MUC(cannot_contain or []),
            'implies_true': MUC(implies_true or []),
            'implies_false': MUC(implies_false or [])
        }
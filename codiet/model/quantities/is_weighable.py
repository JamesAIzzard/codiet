from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.utils.unique_dict import FrozenUniqueDict as FUD
    from codiet.model.quantities import UnitConversion

class IsWeighable(Protocol):
    @property
    def unit_conversions(self) -> "FUD[tuple[str, str], UnitConversion]":
        ...
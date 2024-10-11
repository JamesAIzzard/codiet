from typing import TYPE_CHECKING, TypedDict

from codiet.utils.unique_dict import UniqueDict, FrozenUniqueDict
from codiet.model.quantities import IsWeighable, UnitConversion

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion, UnitConversionDTO
    from codiet.model.cost import QuantityCost, QuantityCostDTO
    from codiet.model.flags import Flag, FlagDTO
    from codiet.model.nutrients import NutrientQuantity, NutrientQuantityDTO


class IngredientDTO(TypedDict):
    name: str
    description: str | None
    unit_conversions: dict[frozenset[str], "UnitConversionDTO"]
    standard_unit: str
    quantity_cost: "QuantityCostDTO"
    gi: float | None
    flags: dict[str, "FlagDTO"]
    nutrient_quantities_per_gram: dict[str, "NutrientQuantityDTO"]


class Ingredient(IsWeighable):

    def __init__(
        self,
        name: str,
        description: str | None,
        unit_conversions: dict[frozenset[str], "UnitConversion"],
        standard_unit: "Unit",
        quantity_cost: "QuantityCost",
        gi: float | None,
        flags: dict[str, "Flag"],
        nutrient_quantities_per_gram: dict[str, "NutrientQuantity"],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._name = name
        self._description = description
        self._unit_conversions = UniqueDict(unit_conversions)
        self._standard_unit = standard_unit
        self._quantity_cost = quantity_cost
        self._gi = gi
        self._flags = UniqueDict(flags)
        self._nutrient_quantities_per_gram = UniqueDict(nutrient_quantities_per_gram)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip().replace(" ", ""):
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, value: str | None) -> None:
        self._description = value

    @property
    def unit_conversions(self) -> FrozenUniqueDict[frozenset[str], "UnitConversion"]:
        return FrozenUniqueDict(self._unit_conversions)

    @property
    def standard_unit(self) -> "Unit":
        return self._standard_unit

    @standard_unit.setter
    def standard_unit(self, unit: "Unit") -> None:
        self._standard_unit = unit

    @property
    def quantity_cost(self) -> "QuantityCost":
        return self._quantity_cost

    @quantity_cost.setter
    def quantity_cost(self, quantity_cost: "QuantityCost") -> None:
        self._quantity_cost = quantity_cost

    @property
    def gi(self) -> float | None:
        return self._gi

    @gi.setter
    def gi(self, value: float | None) -> None:
        if value is not None and (value < 0 or value > 100):
            raise ValueError("GI must be between 0 and 100.")
        self._gi = value

    @property
    def flags(self) -> FrozenUniqueDict[str, "Flag"]:
        return FrozenUniqueDict(self._flags)

    @property
    def nutrient_quantities_per_gram(self) -> FrozenUniqueDict[str, "NutrientQuantity"]:
        return FrozenUniqueDict(self._nutrient_quantities_per_gram)

    def add_unit_conversion(self, unit_conversion: "UnitConversion") -> "Ingredient":
        self._unit_conversions[unit_conversion.unit_names] = unit_conversion
        return self

    def remove_unit_conversion(self, unit_conversion: UnitConversion) -> "Ingredient":
        del self._unit_conversions[unit_conversion.unit_names]
        return self

    def get_flag(self, name: str) -> "Flag":
        return self._flags[name]

    def get_nutrient_quantity_per_gram(self, nutrient_name: str) -> "NutrientQuantity":
        return self._nutrient_quantities_per_gram[nutrient_name]

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

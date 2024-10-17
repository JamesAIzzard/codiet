from typing import TYPE_CHECKING, TypedDict

from codiet.utils.unique_dict import FrozenUniqueDict as FUD
from codiet.utils.unique_dict import UniqueDict as UD
from codiet.model.quantities import IsQuantified
from codiet.model.nutrients import HasNutrientQuantities
from codiet.model.calories import HasCalories
from codiet.model.ingredients import Ingredient

if TYPE_CHECKING:
    from codiet.model.quantities import QuantityDTO, UnitConversionService
    from codiet.model.nutrients import NutrientQuantity, NutrientFactory
    from codiet.model.flags import Flag


class IngredientQuantityDTO(TypedDict):
    ingredient_name: str
    quantity: "QuantityDTO"


class IngredientQuantity(HasCalories, HasNutrientQuantities, IsQuantified):

    unit_conversion_service: "UnitConversionService"
    _nutrient_factory: "NutrientFactory"

    def __init__(self, ingredient: "Ingredient", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._ingredient = ingredient

    @classmethod
    def initialise(
        cls, 
        unit_conversion_service: "UnitConversionService",
        nutrient_factory: "NutrientFactory"
    ) -> None:
        cls.unit_conversion_service = unit_conversion_service
        cls._nutrient_factory = nutrient_factory

    @property
    def ingredient(self) -> "Ingredient":
        return self._ingredient

    @property
    def flags(self) -> "FUD[str, Flag]":
        return self.ingredient.flags

    @property
    def mass_in_grams(self) -> float:
        return self.unit_conversion_service.convert_quantity(
            self.quantity,
            to_unit_name="gram",
            instance_unit_conversions=self.ingredient.unit_conversions,
        ).value

    @property
    def nutrient_quantities(self) -> "FUD[str, NutrientQuantity]":
        nutrient_quantities_totals = UD[str, "NutrientQuantity"]()

        for nutrient_name in self.ingredient.nutrient_quantities_per_gram.keys():
            quantity = self.ingredient.nutrient_quantities_per_gram[nutrient_name].quantity
            quantity_in_grams = self.unit_conversion_service.convert_to_grams(
                quantity=quantity,
                instance_unit_conversions=self.ingredient.unit_conversions
            )
            nutrient_quantities_totals[nutrient_name] = self._nutrient_factory.create_nutrient_quantity(
                nutrient_name=nutrient_name,
                quantity_value=quantity_in_grams.value * self.mass_in_grams,
                quantity_unit_name="gram",
            )

        return FUD(nutrient_quantities_totals)

    def __eq__(self, other):
        if not isinstance(other, IngredientQuantity):
            return False
        return (self.ingredient) == (other.ingredient)

    def __hash__(self):
        return hash(self.ingredient)

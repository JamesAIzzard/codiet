from typing import TYPE_CHECKING, TypedDict

from codiet.utils.unique_dict import FrozenUniqueDict as FUD
from codiet.model.quantities import IsQuantified
from codiet.model.calories import HasCalories
from codiet.model.nutrients import HasNutrientQuantities
from codiet.model.flags import HasFlags

if TYPE_CHECKING:
    from codiet.model.quantities import QuantityDTO, UnitConversionService
    from codiet.model.flags import Flag
    from codiet.model.nutrients import NutrientQuantity
    from codiet.model.recipes.recipe import Recipe


class RecipeQuantityDTO(TypedDict):
    recipe_name: str
    quantity: "QuantityDTO"


class RecipeQuantity(HasCalories, HasNutrientQuantities, HasFlags, IsQuantified):

    unit_conversion_service: "UnitConversionService"

    def __init__(self, recipe: "Recipe", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._recipe = recipe

    @property
    def recipe(self) -> "Recipe":
        return self._recipe

    @property
    def nutrient_quantities(self) -> "FUD[str, NutrientQuantity]":
        nutrient_quantities_totals = {}

        self_mass_grams = self.mass_in_grams

        for nutrient_name, nutrient_quantity in self.recipe.nutrient_quantities.items():
            if nutrient_name in nutrient_quantities_totals:
                nutrient_quantities_totals[nutrient_name] += nutrient_quantity.mass_in_grams * self_mass_grams
            else:
                nutrient_quantities_totals = nutrient_quantity.mass_in_grams * self_mass_grams

        return FUD(nutrient_quantities_totals)

    def get_flag(self, flag_name: str) -> "Flag":
        return self.recipe.get_flag(flag_name)

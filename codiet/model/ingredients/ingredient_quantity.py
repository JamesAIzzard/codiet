from typing import TYPE_CHECKING, TypedDict

from codiet.utils.unique_dict import FrozenUniqueDict as FUD
from codiet.utils.unique_dict import UniqueDict as UD
from codiet.model.quantities import IsQuantified
from codiet.model.nutrients import HasNutrientQuantities
from codiet.model.calories import HasCalories
from codiet.model.ingredients import Ingredient

if TYPE_CHECKING:
    from codiet.model.quantities import QuantityDTO
    from codiet.model.nutrients import NutrientQuantity


class IngredientQuantityDTO(TypedDict):
    ingredient_name: str
    quantity: "QuantityDTO"


class IngredientQuantity(HasCalories, HasNutrientQuantities, IsQuantified):

    def __init__(self, ingredient: "Ingredient", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._ingredient = ingredient

    @property
    def ingredient(self) -> "Ingredient":
        return self._ingredient

    @property
    def nutrient_quantities(self) -> "FUD[str, NutrientQuantity]":
        nutrient_quantities_totals = UD[str, NutrientQuantity]()

        self_mass_grams = self.mass_in_grams

        for nutrient_name, nutrient_quantity in self.ingredient.nutrient_quantities_per_gram.items():
            if nutrient_name in nutrient_quantities_totals:
                nutrient_quantities_totals[nutrient_name] += nutrient_quantity.mass_in_grams * self_mass_grams
            else:
                nutrient_quantities_totals = nutrient_quantity.mass_in_grams * self_mass_grams

        return FUD(nutrient_quantities_totals)

    def __eq__(self, other):
        if not isinstance(other, IngredientQuantity):
            return False
        return (self.ingredient) == (other.ingredient)

    def __hash__(self):
        return hash(self.ingredient)

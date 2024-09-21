from typing import TYPE_CHECKING

from codiet.tests.fixtures import BaseTestFixtures
from .create_test_ingredients import create_test_ingredients
from codiet.model.ingredients import Ingredient, IngredientQuantity

if TYPE_CHECKING:
    from codiet.model.quantities import Quantity

class IngredientTestFixtures(BaseTestFixtures):

    def __init__(self) -> None:

        self._test_ingredients:dict[str, Ingredient]|None = None

    @property
    def ingredients(self) -> dict[str, Ingredient]:
        if self._test_ingredients is None:
            self._test_ingredients = create_test_ingredients()
        return self._test_ingredients
    
    def get_ingredient_by_name(self, ingredient_name:str) -> Ingredient:
        return self.ingredients[ingredient_name]

    def create_ingredient_quantity(self, ingredient_name:str, quantity:'Quantity|None'=None) -> IngredientQuantity:
        ingredient = self.get_ingredient_by_name(ingredient_name)
        return IngredientQuantity(ingredient=ingredient, quantity=quantity)
from typing import TYPE_CHECKING

from codiet.tests.fixtures import BaseTestFixture
from codiet.model.ingredients import Ingredient, IngredientQuantity
from codiet.db_population.ingredients import build_ingredient_from_json
from .utils import fetch_test_ingredient_data

if TYPE_CHECKING:
    from codiet.model.quantities import Quantity

INGREDIENT_NAMES = ["apple", "sugar", "butter", "flour"]

class IngredientTestFixtures(BaseTestFixture):

    def __init__(self) -> None:
        super().__init__()
        self._test_ingredients: dict[str, Ingredient] = {}

    @property
    def ingredients(self) -> dict[str, Ingredient]:
        for name in INGREDIENT_NAMES:
            if name not in self._test_ingredients:
                self._test_ingredients[name] = self.create_test_ingredient(name)
        return self._test_ingredients

    def create_test_ingredient(self, ingredient_name: str) -> Ingredient:
        ingredient_data = fetch_test_ingredient_data(ingredient_name)
        ingredient = build_ingredient_from_json(ingredient_data)
        return ingredient

    def create_test_ingredient_quantity(self, ingredient_name: str, quantity: 'Quantity|None' = None) -> IngredientQuantity:
        ingredient = self.create_test_ingredient(ingredient_name)
        return IngredientQuantity(ingredient=ingredient, quantity=quantity)
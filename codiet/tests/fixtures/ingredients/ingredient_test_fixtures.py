import os
from typing import TYPE_CHECKING

from codiet.utils.json import read_json_data
from codiet.tests.fixtures import BaseTestFixture
from codiet.model.ingredients import Ingredient, IngredientQuantity
from codiet.db_population.ingredients import build_ingredient_from_json

if TYPE_CHECKING:
    from codiet.model.quantities import Quantity

TEST_DATA_DIRNAME = "test_ingredient_data"
TEST_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), TEST_DATA_DIRNAME)

class IngredientTestFixtures(BaseTestFixture):

    def __init__(self) -> None:
        super().__init__()
        self._test_ingredients:dict[str, Ingredient]|None = None

    @property
    def ingredients(self) -> dict[str, Ingredient]:
        if self._test_ingredients is None:
            self._test_ingredients = {
                "apple": self.create_test_ingredient("apple"),
                "sugar": self.create_test_ingredient("sugar"),
                "butter": self.create_test_ingredient("butter"),
                "flour": self.create_test_ingredient("flour"),
            }
        return self._test_ingredients
    
    def create_test_ingredient(self, ingredient_name:str) -> Ingredient:
        ingredient_data = self._fetch_test_ingredient_data(ingredient_name)
        ingredient = build_ingredient_from_json(ingredient_data)
        return ingredient

    def create_ingredient_quantity(self, ingredient_name:str, quantity:'Quantity|None'=None) -> IngredientQuantity:
        ingredient = self.create_test_ingredient(ingredient_name)
        return IngredientQuantity(ingredient=ingredient, quantity=quantity)
    
    def _fetch_test_ingredient_data(self, ingredient_name:str) -> dict:
        return read_json_data(f"{TEST_DATA_FILEPATH}/{ingredient_name}.json")
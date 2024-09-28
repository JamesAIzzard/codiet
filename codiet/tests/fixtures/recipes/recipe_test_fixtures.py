from typing import TYPE_CHECKING

from codiet.tests.fixtures import BaseTestFixture
from codiet.model.recipes import Recipe, RecipeQuantity
# from codiet.db_population.recipes import build_recipe_from_json
from .utils import fetch_test_recipe_data

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe

RECIPE_NAMES = ["apple_pie", "coffee"]

class RecipeTestFixtures(BaseTestFixture):
    
    def __init__(self) -> None:
        super().__init__()
        self._test_recipes: dict[str, Recipe] = {}

    @property
    def recipes(self) -> dict[str, Recipe]:
        for name in RECIPE_NAMES:
            if name not in self._test_recipes:
                self._test_recipes[name] = self.create_test_recipe(name)
        return self._test_recipes

    def get_recipe(self, recipe_name: str) -> Recipe:
        return self.recipes[recipe_name]

    def create_test_recipe(self, recipe_name: str) -> Recipe:
        recipe_data = fetch_test_recipe_data(recipe_name)
        recipe = build_recipe_from_json(recipe_data)
        return recipe
    
    def create_test_recipe_quantity(self, recipe_name: str, quantity: int) -> RecipeQuantity:
        recipe = self.create_test_recipe(recipe_name)
        return RecipeQuantity(recipe=recipe, quantity=quantity)

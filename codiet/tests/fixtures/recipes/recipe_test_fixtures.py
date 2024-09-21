from typing import TYPE_CHECKING

from codiet.tests.fixtures import BaseTestFixtures
from .create_test_recipes import create_test_recipes

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe

class RecipeTestFixtures(BaseTestFixtures):
    
    def __init__(self) -> None:
        self._test_recipes:dict[str, 'Recipe']|None = None

    @property
    def recipes(self) -> dict[str, 'Recipe']:
        if self._test_recipes is None:
            self._test_recipes = create_test_recipes()
        return self._test_recipes
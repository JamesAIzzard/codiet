from typing import TYPE_CHECKING, Callable, Any

from codiet.tests.fixtures import BaseTestFixture
from codiet.model.ingredients import Ingredient, IngredientQuantity

if TYPE_CHECKING:
    from codiet.model.quantities import Quantity
    from codiet.db_population.ingredients import JSONIngredientBuilder

INGREDIENT_NAMES = ["apple", "sugar", "butter", "flour"]

class IngredientTestFixtures(BaseTestFixture):

    # def __init__(self,
    #         json_ingredient_builder: 'JSONIngredientBuilder',
    #         fetch_test_ingredient_data: Callable[[str], dict[str, Any]]
    #     ) -> None:
    #     super().__init__()
    #     self._test_ingredients: dict[str, Ingredient] = {}
    #     self._json_ingredient_builder = json_ingredient_builder
    #     self._fetch_test_ingredient_data = fetch_test_ingredient_data

    def __init__(self) -> None:
        super().__init__()
        self._test_ingredients: dict[str, Ingredient] = {}

    @property
    def ingredients(self) -> dict[str, Ingredient]:
        for name in INGREDIENT_NAMES:
            if name not in self._test_ingredients:
                self._test_ingredients[name] = self.create_test_ingredient(name)
        return self._test_ingredients

    def get_ingredient(self, ingredient_name: str) -> Ingredient:
        return self.ingredients[ingredient_name]

    def create_test_ingredient(self, ingredient_name: str) -> Ingredient:
        ingredient_data = self._fetch_test_ingredient_data(ingredient_name)
        ingredient = self._json_ingredient_builder.build_ingredient(ingredient_data)
        return ingredient

    def create_test_ingredient_quantity(self, ingredient_name: str, quantity: 'Quantity|None' = None) -> IngredientQuantity:
        ingredient = self.create_test_ingredient(ingredient_name)
        return IngredientQuantity(ingredient=ingredient, quantity=quantity)
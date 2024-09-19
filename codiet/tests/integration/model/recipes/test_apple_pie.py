from codiet.tests import BaseModelTest
from codiet.tests.fixtures.quantities import QuantitiesTestFixtures
from codiet.tests.fixtures.ingredients import IngredientTestFixtures
from codiet.tests.fixtures.time import TimeTestFixtures
from codiet.model.recipes import Recipe
from codiet.model.ingredients import IngredientQuantity
from codiet.model.quantities import Quantity
from codiet.model.tags import Tag

class BaseRecipeIntegrationTest(BaseModelTest):

    def setUp(self) -> None:
        super().setUp()
        self.ingredient_fixtures = IngredientTestFixtures()
        self.unit_fixtures = QuantitiesTestFixtures()
        self.time_fixtures = TimeTestFixtures()

class TestMakeApplePie(BaseRecipeIntegrationTest):

    def make_apple_pie(self):
        apple_pie = Recipe("Apple Pie")
        apple_pie.use_as_ingredient = False
        apple_pie.description = "A delicious apple pie."
        apple_pie.instructions = "Bake the apple pie."
        
        ingredient_quantities = self.create_apple_pie_ingredient_quantities()
        for ingredient_quantity in ingredient_quantities:
            apple_pie.add_ingredient_quantity(ingredient_quantity)

        dinner_time = self.time_fixtures.create_time_window("16:00", "23:59")
        apple_pie.add_serve_time_window(dinner_time)

        apple_pie.add_tag(Tag("dessert"))

    def create_apple_pie_ingredient_quantities(self) -> list[IngredientQuantity]:
        return [
            self.ingredient_fixtures.create_ingredient_quantity(
                "apple", Quantity(self.unit_fixtures.get_unit("whole"), 7)
            ),
            self.ingredient_fixtures.create_ingredient_quantity(
                "sugar", Quantity(self.unit_fixtures.get_unit("cup"), 1)
            ),
            self.ingredient_fixtures.create_ingredient_quantity(
                "butter", Quantity(self.unit_fixtures.get_unit("tablespoon"), 2)
            ),
            self.ingredient_fixtures.create_ingredient_quantity(
                "flour", Quantity(self.unit_fixtures.get_unit("cup"), 2.5)
            )
        ]

    def test_can_make_apple_pie(self):
        apple_pie = self.make_apple_pie()
        self.assertIsInstance(apple_pie, Recipe)
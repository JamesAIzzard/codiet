from codiet.model.recipes import Recipe
from codiet.model.quantities import Quantity
from codiet.model.tags import Tag
from codiet.tests.fixtures import BaseTestFixture
from codiet.tests.fixtures.ingredients import IngredientTestFixtures
from codiet.tests.fixtures.time import TimeTestFixtures

class RecipeFactory(BaseTestFixture):
    def __init__(self) -> None:
        super().__init__()
        
        self.ingredient_fixtures = IngredientTestFixtures.get_instance()
        self.time_fixtures = TimeTestFixtures.get_instance()

    def create_apple_pie(self) -> Recipe:

        apple_pie = Recipe("Apple Pie")

        apple_pie.use_as_ingredient = False

        apple_pie.description = "A delicious apple pie."

        apple_pie.instructions = "Bake the apple pie."
        
        apple_pie.add_ingredient_quantity(
            self.ingredient_fixtures.create_test_ingredient_quantity(
                "apple", Quantity("whole", 7)
            )
        )
        apple_pie.add_ingredient_quantity(
            self.ingredient_fixtures.create_test_ingredient_quantity(
                "sugar", Quantity("cup", 1)
            )
        )
        apple_pie.add_ingredient_quantity(
            self.ingredient_fixtures.create_test_ingredient_quantity(
                "butter", Quantity("tablespoon", 2)
            )
        )
        apple_pie.add_ingredient_quantity(
            self.ingredient_fixtures.create_test_ingredient_quantity(
                "flour", Quantity("cup", 2.5)
            )
        )

        dinner_time = self.time_fixtures.create_time_window("16:00", "23:59")
        apple_pie.add_serve_time_window(dinner_time)

        apple_pie.add_tag(Tag("dessert"))

        return apple_pie
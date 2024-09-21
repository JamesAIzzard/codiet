from codiet.model.recipes import Recipe
from codiet.model.ingredients import IngredientQuantity
from codiet.model.quantities import Quantity
from codiet.model.tags import Tag

def create_test_recipes():
    return {
        "apple_pie": create_apple_pie()
    }

def create_apple_pie():
    apple_pie = Recipe("Apple Pie")
    apple_pie.use_as_ingredient = False
    apple_pie.description = "A delicious apple pie."
    apple_pie.instructions = "Bake the apple pie."
    
    ingredient_quantities = create_apple_pie_ingredient_quantities()
    for ingredient_quantity in ingredient_quantities:
        apple_pie.add_ingredient_quantity(ingredient_quantity)

    dinner_time = time_fixtures.create_time_window("16:00", "23:59")
    apple_pie.add_serve_time_window(dinner_time)

    apple_pie.add_tag(Tag("dessert"))

def create_apple_pie_ingredient_quantities() -> list[IngredientQuantity]:
    return [
        ingredient_fixtures.create_ingredient_quantity(
            "apple", Quantity(self.quantities_fixtures.get_unit("whole"), 7)
        ),
        ingredient_fixtures.create_ingredient_quantity(
            "sugar", Quantity(self.quantities_fixtures.get_unit("cup"), 1)
        ),
        self.ingredient_fixtures.create_ingredient_quantity(
            "butter", Quantity(self.quantities_fixtures.get_unit("tablespoon"), 2)
        ),
        self.ingredient_fixtures.create_ingredient_quantity(
            "flour", Quantity(self.quantities_fixtures.get_unit("cup"), 2.5)
        )
    ]

from codiet.model.recipes import Recipe
from codiet.model.quantities import Quantity
from codiet.model.tags import Tag

def create_apple_pie() -> Recipe:
    fixtures = Fixtures.get_instance()

    apple_pie = Recipe("Apple Pie")

    apple_pie.use_as_ingredient = False

    apple_pie.description = "A delicious apple pie."

    apple_pie.instructions = "Bake the apple pie."
    
    apple_pie.add_ingredient_quantity(
        fixtures.create_ingredient_quantity(
            "apple", Quantity("whole", 7)
        )
    )
    apple_pie.add_ingredient_quantity(
        fixtures.create_ingredient_quantity(
            "sugar", Quantity("cup", 1)
        )
    )
    apple_pie.add_ingredient_quantity(
        fixtures.create_ingredient_quantity(
            "butter", Quantity("tablespoon", 2)
        )
    )
    apple_pie.add_ingredient_quantity(
        fixtures.create_ingredient_quantity(
            "flour", Quantity("cup", 2.5)
        )
    )

    dinner_time = time_fixtures.create_time_window("16:00", "23:59")
    apple_pie.add_serve_time_window(dinner_time)

    apple_pie.add_tag(Tag("dessert"))

    return apple_pie
from codiet.model.quantities import UnitConversion, Quantity
from codiet.model.cost import QuantityCost
from codiet.model.ingredients import Ingredient

def create_test_ingredients() -> dict[str, Ingredient]:
    return {
        "apple": create_apple(),
        "chicken": Ingredient("Chicken"),
        "potato": Ingredient("Potato"),
    }

def create_apple() -> Ingredient:
    apple = Ingredient("Apple")
    apple.description = "A delicious fruit."

    apple.add_unit_conversion(UnitConversion(
        (
            Quantity("gram", 200),
            Quantity("whole", 1),
        )
    ))

    apple.standard_unit = "whole"

    apple.set_quantity_cost(QuantityCost(Quantity("whole", 1), 0.5))

    apple.set_flag("vegan", True)
    apple.set_flag("gluten_free", True)
    apple.get_flag("vegan").set_value(True)

    apple.gi = 38
    
    apple.set_nutrient_quantity("carbohydrate", Quantity("gram", 25))
    apple.get_nutrient_quantity("fat").quantity.set_unit("gram").set_value(0.2)

    return apple
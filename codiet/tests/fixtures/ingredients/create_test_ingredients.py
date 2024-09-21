from codiet.model.quantities import UnitConversion, Quantity
from codiet.model.cost import QuantityCost
from codiet.model.ingredients import Ingredient

def create_test_ingredients() -> dict[str, Ingredient]:
    return {
        "apple": create_apple(),
        "sugar": create_sugar(),
        "butter": create_butter(),
        "flour": create_flour()
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

    apple.gi = 38
    
    apple.set_nutrient_quantity("carbohydrate", Quantity("gram", 25))
    apple.set_nutrient_quantity("protein", Quantity("gram", 0.3))
    apple.set_nutrient_quantity("fat", Quantity("gram", 0.2))

    return apple

def create_sugar() -> Ingredient:
    sugar = Ingredient("Sugar")
    sugar.description = "A sweet ingredient."

    sugar.add_unit_conversion(UnitConversion(
        (
            Quantity("gram", 200),
            Quantity("cup", 1),
        )
    ))

    sugar.standard_unit = "cup"

    sugar.set_quantity_cost(QuantityCost(Quantity("cup", 1), 0.5))

    sugar.set_flag("vegan", True)
    sugar.set_flag("gluten_free", True)

    sugar.gi = 65
    
    sugar.set_nutrient_quantity("carbohydrate", Quantity("gram", 200))
    sugar.set_nutrient_quantity("protein", Quantity("gram", 0))
    sugar.set_nutrient_quantity("fat", Quantity("gram", 0))

    return sugar

def create_butter() -> Ingredient:
    butter = Ingredient("Butter")
    butter.description = "A fatty ingredient."

    butter.add_unit_conversion(UnitConversion(
        (
            Quantity("gram", 200),
            Quantity("tablespoon", 1),
        )
    ))

    butter.standard_unit = "tablespoon"

    butter.set_quantity_cost(QuantityCost(Quantity("tablespoon", 1), 0.5))

    butter.set_flag("vegan", False)
    butter.set_flag("gluten_free", True)

    butter.gi = 0
    
    butter.set_nutrient_quantity("carbohydrate", Quantity("gram", 0))
    butter.set_nutrient_quantity("protein", Quantity("gram", 0))
    butter.set_nutrient_quantity("fat", Quantity("gram", 23))

    return butter

def create_flour() -> Ingredient:
    flour = Ingredient("Flour")
    flour.description = "A starchy ingredient."

    flour.add_unit_conversion(UnitConversion(
        (
            Quantity("gram", 200),
            Quantity("cup", 1),
        )
    ))

    flour.standard_unit = "cup"

    flour.set_quantity_cost(QuantityCost(Quantity("cup", 1), 0.5))

    flour.set_flag("vegan", True)
    flour.set_flag("gluten_free", False)

    flour.gi = 85
    
    flour.set_nutrient_quantity("carbohydrate", Quantity("gram", 75))
    flour.set_nutrient_quantity("protein", Quantity("gram", 10))
    flour.set_nutrient_quantity("fat", Quantity("gram", 1))

    return flour
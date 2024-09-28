from typing import Any, Callable, TYPE_CHECKING

from codiet.model.ingredients import Ingredient

if TYPE_CHECKING:
    from codiet.model.quantities import Unit

# Constants for JSON keys
NAME_KEY = "name"
DESCRIPTION_KEY = "description"
UNIT_CONVERSIONS_KEY = "unit_conversions"
STANDARD_UNIT_KEY = "standard_unit"
QUANTITY_COST_KEY = "quantity_cost"
FLAGS_KEY = "flags"
GI_KEY = "gi"
NUTRIENTS_PER_GRAM_KEY = "nutrients_per_gram"

class JSONIngredientBuilder:
    def __init__(self, unit_source: Callable[[str], 'Unit']):
        self.unit_source = unit_source

    def build_ingredient(self, json_data: dict[str, Any]) -> Ingredient:
        ingredient = Ingredient(json_data[NAME_KEY])
        
        ingredient.description = json_data[DESCRIPTION_KEY]
        self.add_unit_conversions(ingredient, json_data[UNIT_CONVERSIONS_KEY])
        ingredient.standard_unit = self.unit_source(json_data[STANDARD_UNIT_KEY])
        ingredient.quantity_cost = build_quantity_cost_from_json(json_data[QUANTITY_COST_KEY])
        self.add_flags(ingredient, json_data[FLAGS_KEY])
        ingredient.gi = json_data[GI_KEY]
        self.add_nutrients(ingredient, json_data[NUTRIENTS_PER_GRAM_KEY])
        
        return ingredient

    def add_unit_conversions(self, ingredient: Ingredient, unit_conversions_data: list) -> None:
        for conversion_data in unit_conversions_data:
            unit_conversion = build_unit_conversion_from_json(conversion_data)
            ingredient.add_unit_conversion(unit_conversion)

    def add_flags(self, ingredient: Ingredient, flags_data: dict[str, bool]) -> None:
        for flag_name, flag_value in flags_data.items():
            ingredient.set_flag(flag_name, flag_value)

    def add_nutrients(self, ingredient: Ingredient, nutrients_data: dict[str, list[str|float]]) -> None:
        for nutrient_name, quantity_data in nutrients_data.items():
            quantity = build_quantity_from_json(quantity_data)
            ingredient.set_nutrient_quantity(
                nutrient_name=nutrient_name,
                quantity=quantity
            )
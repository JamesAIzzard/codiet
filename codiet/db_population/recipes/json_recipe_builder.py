from typing import Any, Callable

from codiet.model.recipes import Recipe
from codiet.model.ingredients import IngredientQuantity
from codiet.model.time import TimeWindow
from codiet.model.tags import Tag
from codiet.db_population.quantities import build_quantity_from_json

# Constants for JSON keys
NAME_KEY = "name"
DESCRIPTION_KEY = "description"
USE_AS_INGREDIENT_KEY = "use_as_ingredient"
INSTRUCTIONS_KEY = "instructions"
INGREDIENTS_KEY = "ingredients"
SERVE_TIME_WINDOW_KEY = "serve_time_windows"
TAGS_KEY = "tags"

class JSONRecipeBuilder:
    def __init__(self, ingredient_source: Callable[[str], Any], unit_source: Callable[[str], Any]):
        self.ingredient_source = ingredient_source
        self.unit_source = unit_source

    def build_recipe_from_json(self, json_data: dict[str, Any]) -> Recipe:
        recipe = Recipe(json_data[NAME_KEY])
        
        recipe.description = json_data[DESCRIPTION_KEY]
        recipe.use_as_ingredient = json_data[USE_AS_INGREDIENT_KEY]
        recipe.instructions = json_data[INSTRUCTIONS_KEY]
        
        self.add_ingredients(recipe, json_data[INGREDIENTS_KEY])
        self.add_serve_time_windows(recipe, json_data[SERVE_TIME_WINDOW_KEY])
        self.add_tags(recipe, json_data[TAGS_KEY])
        
        return recipe

    def add_ingredients(self, recipe: Recipe, ingredients_data: list[dict[str, Any]]) -> None:
        for ingredient_data in ingredients_data:
            ingredient_quantity = IngredientQuantity(
                ingredient=self.ingredient_source(ingredient_data[NAME_KEY]),
                quantity=build_quantity_from_json(ingredient_data["quantity"])
            )
            recipe.add_ingredient_quantity(ingredient_quantity)

    def add_serve_time_windows(self, recipe: Recipe, serve_time_window_data: list[str]) -> None:
        time_window = TimeWindow(start=serve_time_window_data[0], end=serve_time_window_data[1])
        recipe.add_serve_time_window(time_window)

    def add_tags(self, recipe: Recipe, tags_data: list[str]) -> None:
        for tag_name in tags_data:
            tag = Tag(name=tag_name)
            recipe.add_tag(tag)
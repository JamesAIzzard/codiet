import os

OPENAI_MODEL = "gpt-3.5-turbo"
GLOBAL_FLAG_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), "global_flags.json")
GLOBAL_NUTRIENT_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), "nutrient_data.json")
GLOBAL_RECIPE_TYPE_DATA_FILEPATH = os.path.join(
    os.path.dirname(__file__), "global_recipe_types.json"
)
RECIPE_TEMPLATE_FILEPATH = os.path.join(os.path.dirname(__file__), "recipe_template.json")
RECIPE_INGREDIENT_TEMPLATE_FILEPATH = os.path.join(
    os.path.dirname(__file__), "recipe_ingredient_template.json"
)
INGREDIENT_TEMPLATE_FILEPATH = os.path.join(
    os.path.dirname(__file__), "ingredient_template.json"
)
INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), "ingredient_data")
RECIPE_DATA_DIR = os.path.join(os.path.dirname(__file__), "recipe_data")
INGREDIENT_WISHLIST_FILEPATH = os.path.join(
    os.path.dirname(__file__), "ingredient_wishlist.json"
)

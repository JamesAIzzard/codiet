import os

OPENAI_MODEL = "gpt-3.5-turbo"
FLAG_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), "global_flags.json")
NUTRIENT_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), "nutrient_data.json")
RECIPE_TYPE_DATA_FILE = os.path.join(
    os.path.dirname(__file__), "global_recipe_types.json"
)
INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), "ingredient_data")
INGREDIENT_WISHLIST_FILEPATH = os.path.join(
    os.path.dirname(__file__), "ingredient_wishlist.json"
)
INGREDIENT_TEMPLATE_FILEPATH = os.path.join(
    os.path.dirname(__file__), "ingredient_template.json"
)
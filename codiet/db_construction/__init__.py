import os

OPENAI_MODEL = "gpt-3.5-turbo"
FLAG_DATA_FILE = os.path.join(os.path.dirname(__file__), "global_flags.json")
NUTRIENT_DATA_FILE = os.path.join(os.path.dirname(__file__), "nutrient_data.json")
INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), "ingredient_data")
INGREDIENT_WISHLIST_FILE = os.path.join(
    os.path.dirname(__file__), "ingredient_wishlist.json"
)
INGREDIENT_TEMPLATE_FILE = os.path.join(
    os.path.dirname(__file__), "ingredient_template.json"
)
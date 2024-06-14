import os

OPENAI_MODEL = "gpt-4o"
GLOBAL_FLAG_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), "global_flags.json")
GLOBAL_NUTRIENT_DATA_FILEPATH = os.path.join(
    os.path.dirname(__file__), "nutrient_data.json"
)
INGREDIENT_TEMPLATE_DIR = os.path.join(
    os.path.dirname(__file__), "ingredient_datafile_templates"
)
INGREDIENT_TEMPLATE_FILEPATH = os.path.join(
    INGREDIENT_TEMPLATE_DIR, "ingredient_data_template.json"
)
INGREDIENT_COST_TEMPLATE_FILEPATH = os.path.join(
    INGREDIENT_TEMPLATE_DIR, "ingredient_cost_data_template.json"
)
INGREDIENT_CUSTOM_UNITS_TEMPLATE_FILEPATH = os.path.join(
    INGREDIENT_TEMPLATE_DIR, "ingredient_custom_unit_data_template.json"
)
INGREDIENT_NUTRIENT_QUANTITY_TEMPLATE_FILEPATH = os.path.join(
    INGREDIENT_TEMPLATE_DIR, "ingredient_nutrient_quantity_data_template.json"
)
INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), "ingredient_data")
RECIPE_DATA_DIR = os.path.join(os.path.dirname(__file__), "recipe_data")
INGREDIENT_WISHLIST_FILEPATH = os.path.join(
    os.path.dirname(__file__), "ingredient_wishlist.json"
)
GLOBAL_RECIPE_TAG_DATA_FILEPATH = os.path.join(
    os.path.dirname(__file__), "global_recipe_tags.json"
)
RECIPE_TEMPLATE_FILEPATH = os.path.join(
    os.path.dirname(__file__), "recipe_template.json"
)
RECIPE_INGREDIENT_TEMPLATE_FILEPATH = os.path.join(
    os.path.dirname(__file__), "recipe_ingredient_template.json"
)

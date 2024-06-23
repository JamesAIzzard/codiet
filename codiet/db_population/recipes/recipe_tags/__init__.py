import json
import os

GLOBAL_RECIPE_TAGS_FILENAME = 'global_recipe_tags.json'
GLOBAL_RECIPE_TAGS_FILEPATH = os.path.join(os.path.dirname(__file__), GLOBAL_RECIPE_TAGS_FILENAME)

def get_global_recipe_tags() -> dict[str, dict]:
    """Returns a list of global recipe tag names as strings."""
    with open(GLOBAL_RECIPE_TAGS_FILEPATH, 'r') as file:
        return json.load(file)
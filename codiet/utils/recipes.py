import json, os, copy

from codiet.utils.time import convert_datetime_interval_to_time_string_interval
from codiet.models.recipes import Recipe
from codiet.db_construction import (
    RECIPE_TEMPLATE_FILEPATH, 
    RECIPE_INGREDIENT_TEMPLATE_FILEPATH,
    RECIPE_DATA_DIR
)

_recipe_template = None
_recipe_ingredient_template = None

def load_recipe_json_template() -> dict:
    """
    Returns a copy of the recipe template as a dictionary.
    Caches the template for future use.
    """
    global _recipe_template
    if _recipe_template is None:
        # Open the datafile from the recipe template
        with open(RECIPE_TEMPLATE_FILEPATH, "r") as file:
            # Cache the template
            _recipe_template = json.load(file)
    # Return a copy of the template
    return copy.deepcopy(_recipe_template)
        
def load_recipe_ingredient_template() -> dict:
    """
    Returns a copy of the recipe ingredient template as a dictionary.
    Caches the template for future use.
    """
    global _recipe_ingredient_template
    if _recipe_ingredient_template is None:
        # Open the datafile from the recipe template
        with open(RECIPE_INGREDIENT_TEMPLATE_FILEPATH, "r") as file:
            # Cache the template
            _recipe_ingredient_template = json.load(file)
    # Return a copy of the template
    return copy.deepcopy(_recipe_ingredient_template)

def convert_recipe_to_json(recipe: Recipe) -> dict:
    """Convert a recipe to a JSON serializable dictionary."""
    # Create a dictionary to store the recipe
    recipe_data = load_recipe_json_template()
    # Populate the name, description, and instructions
    recipe_data["name"] = recipe.name
    recipe_data["description"] = recipe.description
    recipe_data["instructions"] = recipe.instructions
    # Add the ingredients to the recipe dictionary
    for ingredient_id, ingredient_qty in recipe.ingredient_quantities.items():
        # Fetch the ingredient quantity template
        ingredient_template = load_recipe_ingredient_template()
        # Populate the ingredient template
        ingredient_template["id"] = ingredient_qty.ingredient.id
        ingredient_template["qty_unit"] = ingredient_qty.qty_unit
        ingredient_template["qty_value"] = ingredient_qty.qty_value
        ingredient_template["qty_upper_tol"] = ingredient_qty.upper_tol
        ingredient_template["qty_lower_tol"] = ingredient_qty.lower_tol
        # Add the ingredient to the recipe dictionary
        recipe_data["ingredients"][ingredient_qty.ingredient.id] = ingredient_template
    # Add the serve times to the recipe dictionary
    for serve_time in recipe.serve_times:
        # Convert the serve time to a string
        timestring_interval = convert_datetime_interval_to_time_string_interval(serve_time)
        recipe_data["serve_times"].append(timestring_interval)
    # Add the recipe types to the recipe dictionary
    for recipe_type in recipe.recipe_types:
        recipe_data["types"].append(recipe_type)
    # Return the recipe dictionary
    return recipe_data

def save_recipe_datafile(datafile:dict) -> None:
    """Save the datafile into the recipe data directory."""
    # Raise an exception if the name is None or an empty string
    if datafile["name"] is None or datafile["name"] == "":
        raise ValueError("Recipe name cannot be None or an empty string.")
    # Convert the recipe name to snake case
    filename = datafile["name"].replace(" ", "_").lower()
    # Raise an exception if the datafile already exists
    if recipe_datafile_exists(filename):
        raise FileExistsError(f"Recipe datafile '{filename}.json' already exists.")
    # Create the filepath for the recipe datafile
    recipe_data_filepath = os.path.join(RECIPE_DATA_DIR, f"{filename}.json")
    # Write the datafile to the recipe data directory
    with open(recipe_data_filepath, "w") as file:
        json.dump(datafile, file, indent=4)

def recipe_datafile_exists(datafile_name:str) -> bool:
    """Check if a recipe datafile exists."""
    # Return True if the recipe datafile exists
    return os.path.exists(os.path.join(RECIPE_DATA_DIR, f"{datafile_name}.json"))
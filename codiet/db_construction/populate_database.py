"""
Module containing functions to push the source data .json files
into the database.
"""

import os, json

from codiet.db_construction import (
    INGREDIENT_DATA_DIR,
    RECIPE_DATA_DIR,
    GLOBAL_FLAG_DATA_FILEPATH,
    GLOBAL_NUTRIENT_DATA_FILEPATH,
    GLOBAL_RECIPE_TYPE_DATA_FILEPATH
)
from codiet.models.ingredients import Ingredient, IngredientNutrientQuantity
from codiet.models.recipes import Recipe
from codiet.db.database_service import DatabaseService

def push_flags_to_db():
    """Populate the flags table in the database using the 
    .json flag list file."""
    # Read the flags from the datafile
    with open(GLOBAL_FLAG_DATA_FILEPATH) as file:
        flags = json.load(file)
    # Push the flags to the database
    with DatabaseService() as db_service:
        db_service.insert_global_flags(flags)
        # Save changes
        db_service.commit()

def push_nutrients_to_db():
    """Populate the database with nutrient data."""
    # Read the nutrient data from the file
    with open(GLOBAL_NUTRIENT_DATA_FILEPATH) as file:
        nutrient_data = json.load(file)
    # Define a recursive function to insert either a leaf or a group nutrient
    def insert_nutrients(nutrient_data:dict, db_service:DatabaseService, parent_id:int|None=None):
        """Recursively insert the nutrient data into the database."""
        for nutrient_name, data in nutrient_data.items():
            # Check if the current item is a group (has children) or a leaf (no children)
            if data["children"]:
                # It's a group nutrient, insert it using the group nutrient method
                # This method returns a unique ID which will be used as the parent ID for its children
                new_parent_id = db_service.insert_global_group_nutrient(nutrient_name, parent_id)
                # Recursively insert the children
                insert_nutrients(data["children"], db_service, new_parent_id)
            else:
                # It's a leaf nutrient, insert it using the leaf nutrient method
                db_service.insert_global_leaf_nutrient(nutrient_name, parent_id)
    # Call the recursive function
    with DatabaseService() as db_service:
        insert_nutrients(nutrient_data, db_service)
        # Save changes
        db_service.commit()

def push_ingredients_to_db():
    """Populate the database with ingredients from the .json ingredient files."""
    with DatabaseService() as db_service:
        # Work through each .json file in the ingredient_data directory
        for file in os.listdir(INGREDIENT_DATA_DIR):
            # Open the file and load the data
            with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
                data = json.load(f)
            # Convert the data into an ingredient instance
            ingredient = _load_ingredient_from_json(data)
            # Save the ingredient to the database
            db_service.insert_new_ingredient(ingredient)
            # Save changes
            db_service.commit()


def push_global_recipe_types_to_db():
    """Push the global recipe types to the database."""
    # Read the global recipe types from the file
    with open(GLOBAL_RECIPE_TYPE_DATA_FILEPATH) as file:
        global_recipe_types = json.load(file)
    # Add each recipe type to the database
    with DatabaseService() as db_service:
        for recipe_type in global_recipe_types:
            db_service.insert_global_recipe_type(recipe_type)
        # Save changes
        db_service.commit()
    print("Global recipe types pushed to the database.")

def push_recipes_to_db():
    """Push the recipes to the database."""
    # For each of the recipe datafiles
    for file in os.listdir(RECIPE_DATA_DIR):
        # Open the file and load the data
        with open(os.path.join(RECIPE_DATA_DIR, file)) as f:
            data = json.load(f)
        # Convert the data into a recipe instance
        recipe = _load_recipe_from_json(data)
        # Save the recipe to the database
        with DatabaseService() as db_service:
            db_service.insert_new_recipe(recipe)
            # Save changes
            db_service.commit()

def _load_ingredient_from_json(json_data) -> Ingredient:
    """Load an ingredient object from a json data dict."""
    # Create the ingredient instance
    with DatabaseService() as db_service:
        ingredient = db_service.create_empty_ingredient()
    # Move the ingredient data into the instance
    ingredient.name = json_data["name"]
    ingredient.description = json_data["description"]
    ingredient.cost_unit = json_data["cost"]["cost_unit"]
    ingredient.cost_value = json_data["cost"]["cost_value"]
    ingredient.cost_qty_unit = json_data["cost"]["qty_unit"]
    ingredient.cost_qty_value = json_data["cost"]["qty_value"]
    ingredient.density_mass_unit = json_data["bulk"]["density"]["mass_unit"]
    ingredient.density_mass_value = json_data["bulk"]["density"]["mass_value"]
    ingredient.density_vol_unit = json_data["bulk"]["density"]["vol_unit"]
    ingredient.density_vol_value = json_data["bulk"]["density"]["vol_value"]
    ingredient.set_flags(json_data["flags"])
    ingredient.gi = json_data["GI"]
    # For each of the nutrient dicts, create an IngredientNutrientQuantity
    # instance and add it to the ingredient
    for nutrient_name, nutrient_data in json_data["nutrients"].items():
        nutrient_qty = _load_ingredient_nutrient_qty_from_json(nutrient_name, nutrient_data)
        ingredient.update_nutrient_quantity(nutrient_qty)
    return ingredient

def _load_ingredient_nutrient_qty_from_json(nutrient_name:str, nutrient_data:dict) -> IngredientNutrientQuantity:
    """Load an ingredient nutrient quantity object from a json data dict."""
    # Create the ingredient nutrient quantity instance
    nutrient_qty = IngredientNutrientQuantity(
        name=nutrient_name,
        ntr_mass_value=nutrient_data["ntr_qty_value"],
        ntr_mass_unit=nutrient_data["ntr_qty_unit"],
        ing_qty_value=nutrient_data["ing_qty_value"],
        ing_qty_unit=nutrient_data["ing_qty_unit"]
    )
    return nutrient_qty

def _load_recipe_from_json(json_data) -> Recipe:
    """Load a recipe object from a json data dict."""
    # Create the recipe instance
    recipe = Recipe()
    # Move the recipe data into the instance
    recipe.name = json_data["name"]
    recipe.description = json_data["description"]
    return recipe
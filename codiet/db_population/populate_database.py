"""
Module containing functions to push the source data .json files
into the database.
"""

import os, json

from codiet.db_population import (
    INGREDIENT_DATA_DIR,
    RECIPE_DATA_DIR,
    GLOBAL_CUSTOM_UNIT_DATA_FILEPATH,
    GLOBAL_FLAG_DATA_FILEPATH,
    GLOBAL_NUTRIENT_DATA_FILEPATH,
    GLOBAL_RECIPE_TAG_DATA_FILEPATH,
)
from codiet.utils.tags import flatten_tree
from codiet.models.ingredients import IngredientNutrientQuantity
from codiet.models.recipes import Recipe
from codiet.db.database_service import DatabaseService

def push_global_custom_units_to_db() -> None:
    """Populate the custom units table in the database using the
    .json custom unit list file."""
    # Get the list of custom units
    custom_units = get_global_custom_units()
    # Push the custom units to the database
    with DatabaseService() as db_service:
        db_service.insert_global_custom_units(custom_units)
        # Save changes
        db_service.commit()

def push_global_flags_to_db():
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


def push_global_nutrients_to_db():
    """Populate the database with nutrient data."""
    # Read the nutrient data from the file
    with open(GLOBAL_NUTRIENT_DATA_FILEPATH) as file:
        nutrient_data = json.load(file)

    # Define a recursive function to insert either a leaf or a group nutrient
    def insert_nutrients(
        nutrient_data: dict, db_service: DatabaseService, parent_id: int | None = None
    ):
        """Recursively insert the nutrient data into the database."""
        for nutrient_name, data in nutrient_data.items():
            # Check if the current item is a group (has children) or a leaf (no children)
            if data["children"]:
                # It's a group nutrient, insert it using the group nutrient method
                # This method returns a unique ID which will be used as the parent ID for its children
                new_parent_id = db_service.insert_global_group_nutrient(
                    nutrient_name, parent_id
                )
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
                ingredient_data = json.load(f)
                push_ingredient_to_db(ingredient_data)


def push_ingredient_to_db(ingredient_data: dict):
    """Push the ingredient from the datafile into the database."""
    with DatabaseService() as db_service:
        # Init the ingredient in the database
        ingredient = db_service.insert_new_ingredient(name=ingredient_data["name"])
        # Set the description
        db_service.update_ingredient_description(
            ingredient.id, ingredient_data["description"]
        )
        # Set the cost
        db_service.update_ingredient_cost(
            ingredient.id,
            cost_unit=ingredient_data["cost"]["cost_unit"],
            cost_value=ingredient_data["cost"]["cost_value"],
            cost_qty_value=ingredient_data["cost"]["qty_value"],
            cost_qty_unit=ingredient_data["cost"]["qty_unit"],
        )
        # Add the custom units
        for unit_name, custom_unit_data in ingredient_data["custom_units"].values():
            # Init the custom unit in the database
            custom_unit = db_service.insert_ingredient_custom_unit(
                ingredient.id, unit_name=unit_name
            )
            # Set the custom unit data
            custom_unit.custom_unit_qty = custom_unit_data["custom_unit_qty"]
            custom_unit.std_unit_qty = custom_unit_data["std_unit_qty"]
            custom_unit.std_unit_name = custom_unit_data["std_unit_name"]
            # Update the custom unit in the database
            db_service.update_custom_unit(custom_unit)
        # Add the flags
        for flag_name, flag_value in ingredient_data["flags"].items():
            db_service.update_ingredient_flag(ingredient.id, flag_name, flag_value)
        # Set the GI
        db_service.update_ingredient_gi(ingredient.id, ingredient_data["GI"])
        # Add the nutrients
        # Create a dict relating global nutrient ID's to names
        nutrient_IDs = {}
        for nutrient_name in ingredient_data["nutrients"].keys():
            nutrient_IDs[nutrient_name] = db_service.fetch_leaf_nutrient_id_from_name(
                nutrient_name
            )
        # Add the nutrient quantities to the database
        for nutrient_name, nutrient_data in ingredient_data["nutrients"].items():
            # Init the nutrient in the database
            nutrient = db_service.insert_ingredient_nutrient_quantity(
                ingredient_id=ingredient.id,
                global_nutrient_id=nutrient_IDs[nutrient_name],
            )
            # Set the nutrient data
            nutrient.nutrient_mass_value = nutrient_data["ntr_mass_value"]
            nutrient.ntr_mass_unit = nutrient_data["ntr_mass_unit"]
            nutrient.ing_qty_value = nutrient_data["ing_qty_value"]
            nutrient.ing_qty_unit = nutrient_data["ing_qty_unit"]
            # Update the nutrient in the database
            db_service.update_ingredient_nutrient_quantity(nutrient)
        # Save changes
        db_service.commit()


def push_global_recipe_tags_to_db():
    """Push the global recipe tags to the database."""
    # Read the global recipe tags from the file
    with open(GLOBAL_RECIPE_TAG_DATA_FILEPATH) as file:
        global_recipe_tags = json.load(file)
    # Flatten to list
    flat_global_recipe_tags = flatten_tree(global_recipe_tags)
    # Add each recipe tage to the database
    with DatabaseService() as db_service:
        for recipe_tag in flat_global_recipe_tags:
            db_service.insert_global_recipe_tag(recipe_tag)
        # Save changes
        db_service.commit()
    print("Global recipe tags pushed to the database.")


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


def _load_ingredient_nutrient_qty_from_json(
    nutrient_name: str, nutrient_data: dict
) -> IngredientNutrientQuantity:
    """Load an ingredient nutrient quantity object from a json data dict."""
    # Create the ingredient nutrient quantity instance
    nutrient_qty = IngredientNutrientQuantity(
        nutrient_name=nutrient_name,
        ntr_mass_value=nutrient_data["ntr_mass_value"],
        ntr_mass_unit=nutrient_data["ntr_mass_unit"],
        ing_qty_value=nutrient_data["ing_qty_value"],
        ing_qty_unit=nutrient_data["ing_qty_unit"],
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

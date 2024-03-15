import os, json
from typing import Optional

from codiet.models.ingredient import Ingredient
from codiet.db.database_service import DatabaseService

INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), "ingredient_data")


def _populate_flags(db_service: DatabaseService):
    # Define list of flags
    flags = [
        "alcohol free",
        "caffeine free",
        "gluten free",
        "lactose free",
        "nut free",
        "vegan",
        "vegetarian",
    ]
    # Add each flag to the database
    for flag in flags:
        db_service.repo.insert_flag_into_database(flag)


def _populate_ingredients(db_service: DatabaseService):
    # Work through each .json file in the ingredient_data directory
    for file in os.listdir(INGREDIENT_DATA_DIR):
        # Open the file and load the data
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)

        # Grab the ingredient name
        ingredient_name = data["name"]

        # Create an ingredient instance
        ingredient = Ingredient(ingredient_name)

        # Add the cost data
        ingredient.cost_unit = data["cost"]["cost_unit"]
        ingredient.cost_value = data["cost"]["cost_value"]
        ingredient.cost_qty_unit = data["cost"]["qty_unit"]
        ingredient.cost_qty_value = data["cost"]["qty_value"]

        # Add the density data
        ingredient.density_mass_unit = data["bulk"]["density"]["mass_unit"]
        ingredient.density_mass_value = data["bulk"]["density"]["mass_value"]
        ingredient.density_vol_unit = data["bulk"]["density"]["vol_unit"]
        ingredient.density_vol_value = data["bulk"]["density"]["vol_value"]

        # Add the flags
        ingredient.flags = data["flags"]

        # Add the nutrients
        ingredient.nutrients = data["nutrients"]

        # Save the ingredient
        db_service.create_ingredient(ingredient)

def _populate_nutrients(db_service: DatabaseService):
    # Load the dict from the nutrient_data.json file
    with open(os.path.join(os.path.dirname(__file__), "nutrient_data.json")) as f:
        data = json.load(f)

    # Create a dict to match nutrient names and ID's
    nutrient_ids = {}

    # Create a function to recursively add nutrients
    def _add_nutrient(name: str, data: dict, parent_id: Optional[int]):
        # Add the nutrient to the database, stashing the id
        nutrient_id = db_service.repo.insert_nutrient(name, parent_id)
        # Stash the nutrients ID in the dict
        nutrient_ids[name] = nutrient_id
        # Grab the child elements
        children = data["children"]
        # Add each child   
        for nutrient_name, nutrient_data in children.items():
            # Get parent's ID
            parent_id = nutrient_ids[name]
            # Add the nutrient
            _add_nutrient(nutrient_name, nutrient_data, parent_id=parent_id)
        # Grab any associated aliases
        aliases = data.get("aliases", [])
        # Add each alias
        for alias in aliases:
            db_service.repo.insert_nutrient_alias(alias, nutrient_id)

    # Add each nutrient
    for nutrient_name, nutrient_data in data.items():
        # Add the nutrient
        _add_nutrient(nutrient_name, nutrient_data, None)

    # Commit the changes
    db_service.repo.db.commit()
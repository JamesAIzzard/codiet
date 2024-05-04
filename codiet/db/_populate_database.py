import os, json
from typing import Optional

import openai

from codiet.models.nutrients import create_nutrient_dict
from codiet.db.database_service import DatabaseService

INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), "ingredient_data")
NUTRIENT_DATA_PATH = os.path.join(os.path.dirname(__file__), "nutrient_data.json")


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
        ingredient = db_service.create_empty_ingredient()

        # Set the ingredient name
        ingredient.name = ingredient_name

        # Set the ingredient description
        ingredient.description = data["description"]

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
        ingredient.set_flags(data["flags"])

        # Add the nutrients
        ingredient.nutrients = data["nutrients"]

        # Save the ingredient
        db_service.create_ingredient(ingredient)

def _populate_nutrients(db_service: DatabaseService):
    # Load the dict from the nutrient_data.json file
    with open(NUTRIENT_DATA_PATH) as f:
        data = json.load(f)

    # Create a dict to match nutrient names and ID's
    nutrient_ids = {}

    # Create a list of nutrients which are leaves (have no children)
    leaf_nutrients = _find_leaf_nutrients(data)

    # Create a function to recursively add nutrients
    def _add_nutrient(name: str, data: dict, parent_id: Optional[int]):
        # Add the nutrient to the database, stashing the id
        nutrient_id = db_service.repo.insert_nutrient(
            name, 
            parent_id,
            is_leaf=name in leaf_nutrients
        )
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

def _find_leaf_nutrients(data, leaf_nutrients=None):
    """Recursively find all leaf nutrients in a nested dictionary."""
    # Initialize the list of leaf nutrients on the first call
    if leaf_nutrients is None:
        leaf_nutrients = []

    for key, value in data.items():
        # Check if the current item has children
        if value.get('children'):
            # Recursively call the function with the children
            _find_leaf_nutrients(value['children'], leaf_nutrients)
        else:
            # If no children, add the nutrient to the leaf_nutrients list
            leaf_nutrients.append(key)

    return leaf_nutrients

def _update_ingredient_files(db_service: DatabaseService):
    """Work through each ingredient file in the ingredients data directory
    and make sure:
    - Its flags match those in the database
    - Its nutrients match the leaf nutrients in the database
    """
    # Grab the list of flags from the database
    flags_list = db_service.repo.fetch_all_flag_names()

    # Grab the list of leaf nutrients from the database
    leaf_nutrients_list = db_service.repo.fetch_all_leaf_nutrient_names()

    # For each ingredient file in the directory
    for file in os.listdir(INGREDIENT_DATA_DIR):
        # Open the file and load the data
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)

        print(f"Updating {file}...")

        # Update the flags
        # Create a fresh flag dict
        updated_flags = {}
        # Cycle through each flag from the database
        for flag in flags_list:
            # Try and read the data from the file
            try:
                # If the flag is in the file, add it to the updated flags dict
                updated_flags[flag] = data["flags"][flag]
            except KeyError:
                # If the flag is not in the file, add it with a value of False
                updated_flags[flag] = False
        # Replace the old flags dict with the new
        data["flags"] = updated_flags

        # Update the nutrients
        # Create a fresh nutrient dict
        updated_nutrients = {}
        # Cycle through each leaf nutrient from the database
        for nutrient in leaf_nutrients_list:
            # Try and read the data from the file
            try:
                # If the nutrient is in the file, add it to the updated nutrients dict
                updated_nutrients[nutrient] = data["nutrients"][nutrient]
            except KeyError:
                # If the nutrient is not in the file, remove it
                updated_nutrients[nutrient] = create_nutrient_dict()

        # Replace the old nutrients dict with the new
        data["nutrients"] = updated_nutrients

        # Write the updated data back to the file
        with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
            json.dump(data, f, indent=4)

def _populate_ingredient_data(data: dict) -> dict:
    """Use the GPT-3 API to populate the missing datafields"""
    # Grab the ingredient name
    ingredient_name = data["name"]

    # Replace 'your_api_key_here' with your actual OpenAI API key
    openai.api_key = 'your_api_key_here'

    # The prompt asking for a description of Wholegrain Rice
    prompt = "Provide a detailed description of the ingredient: Wholegrain Rice."

    # Call the OpenAI API with the prompt
    response = openai.Completion.create(
    engine="text-davinci-003",  # You can use the latest available model
    prompt=prompt,
    max_tokens=100  # Adjust the number of tokens as needed
    )

    # Extract the text from the response
    description = response.choices[0].text.strip()

    print(description)

    return data
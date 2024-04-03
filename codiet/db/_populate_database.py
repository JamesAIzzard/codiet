import os, json
from typing import Optional

from openai import OpenAI

from codiet.models.nutrients import create_nutrient_dict
from codiet.db.database_service import DatabaseService

INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), "ingredient_data")
INGREDIENT_WISHLIST = os.path.join(os.path.dirname(__file__), "ingredient_wishlist.json")
INGREDIENT_TEMPLATE = os.path.join(os.path.dirname(__file__), "ingredient_template.json")
NUTRIENT_DATA_PATH = os.path.join(os.path.dirname(__file__), "nutrient_data.json")


def push_flags_to_db(db_service: DatabaseService):
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


def push_ingredients_to_db(db_service: DatabaseService):
    """Populate the database with ingredients from the ingredient_data directory."""
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

def push_nutrients_to_db(db_service: DatabaseService):
    """Populate the database with nutrients from the nutrient_data.json files."""
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

def init_ingredient_datafiles(db_service: DatabaseService):
    """Work through the wishlist and initialise a corresponding ingredient .json file."""
    
    # Read the ingredient_wishlist.json file
    with open(os.path.join(os.path.dirname(__file__), "ingredient_wishlist.json")) as f:
        wishlist = json.load(f)

    # Read the ingredient template file
    with open(os.path.join(os.path.dirname(__file__), "ingredient_template.json")) as f:
        template = json.load(f)

    # For each ingredient in the wishlist
    for ingredient in wishlist:
        # Create the ingredient file name from the ingredient name
        file_name = ingredient.replace(" ", "_").lower() + ".json"

        # Create a .json file with this name, overwriting if it already exists
        with open(os.path.join(INGREDIENT_DATA_DIR, file_name), "w") as f:
            # Make a copy of the entire template
            template = template.copy()

            # Set the name of the ingredient
            template["name"] = ingredient

            # Write the template data to the file
            json.dump(template, f, indent=4)

    # Clear the ingredient wishlist
    with open(os.path.join(os.path.dirname(__file__), "ingredient_wishlist.json"), "w") as f:
        json.dump([], f)


def populate_ingredient_datafiles(db_service: DatabaseService):
    """Work through each ingredient file in the ingredients data directory
    and use the openai API to populate its data."""
    # For each ingredient file in the directory
    for file in os.listdir(INGREDIENT_DATA_DIR):
        # Open the file and load the data
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)

        # Grab the ingredient name
        ingredient_name = data["name"]

        # If the description isn't filled
        if not data.get("description").strip():
            # Update the terminal
            print(f"Getting description for {ingredient_name}...")
            # Use the openai API to get the description
            description = _get_openai_ingredient_description(ingredient_name)
            # Write the description back to the file
            data["description"] = description

            # Save the updated data back to the file
            with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
                json.dump(data, f, indent=4)

        # If the cost data isn't filled, use the openai API to get the cost data
        if data["cost"]["cost_value"] is None:
            print(f"Getting cost data for {ingredient_name}...")
            cost_per_100_g = _get_openai_ingredient_cost_per_100g(ingredient_name)

            # Write the cost data back to the file
            data["cost"]["cost_value"] = float(cost_per_100_g)
            data["cost"]["qty_unit"] = "g"
            data["cost"]["qty_value"] = "100"

            # Save the updated data back to the file
            with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
                json.dump(data, f, indent=4)

        # If the flag data isn't filled, use the openai API to get the flag data
        if len(data["flags"]) == 0:
            print(f"Getting flags for {ingredient_name}...")
            flags = _get_openai_ingredient_flags(ingredient_name, db_service.repo.fetch_all_flag_names())

            # Write the flags back to the file
            data["flags"] = flags

            # Save the updated data back to the file
            with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
                json.dump(data, f, indent=4)

        # If the GI data isn't filled, use the openai API to get the GI data
        if data.get("GI") is None:
            print(f"Getting GI data for {ingredient_name}...")
            gi = _get_openai_ingredient_gi(ingredient_name)

            # Write the GI data back to the file
            data["GI"] = gi

            # Save the updated data back to the file
            with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
                json.dump(data, f, indent=4)

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

def _get_openai_ingredient_description(ingredient_name: str) -> str:
    """Use the OpenAI API to generate a description for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Set the prompt
    prompt = f"Generate a single sentence description for the ingredient '{ingredient_name}'."

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model="gpt-4",
    )

    return chat_completion.choices[0].message.content # type: ignore

def _get_openai_ingredient_cost_per_100g(ingredient_name: str) -> str:
    """Use the OpenAI API to generate a description for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Set the prompt
    prompt = f"By responding with a single decimal only, what is the approximate cost in GBP of 100g of '{ingredient_name}'? It is acceptable to guess, you don't need to access real time data."

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model="gpt-4",
    )

    return chat_completion.choices[0].message.content # type: ignore

def _get_openai_ingredient_flags(ingredient_name: str, flag_list:list[str]) -> dict[str, bool]:
    """Use the OpenAI API to generate a list of flags for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Construct the flag dict with False values
    flags_dict = {flag: False for flag in flag_list}

    # Set the prompt
    prompt = f"Can you populate this list of flags for {ingredient_name}: {json.dumps(flags_dict, indent=4)}? If you are unsure, please leave the flag as False."
    # prompt = f"Generate a list of flags for the ingredient '{ingredient_name}'."

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model="gpt-4",
    )

    # Parse the response
    response = chat_completion.choices[0].message.content # type: ignore
    # Convert the response to a dict
    flags_dict = json.loads(response) # type: ignore

    return flags_dict

def _get_openai_ingredient_gi(ingredient_name: str) -> str:
    """Use the OpenAI API to generate a description for an ingredient."""
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("CODIET_OPENAI_API_KEY"))

    # Set the prompt
    prompt = f"By responding with a single decimal only, what is the approximate Glycemic Index (GI) of '{ingredient_name}'? It is acceptable to guess, you don't need to access real time data."

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model="gpt-4",
    )

    return chat_completion.choices[0].message.content # type: ignore
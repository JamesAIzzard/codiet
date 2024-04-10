import os, json
from json.decoder import JSONDecodeError

from codiet.db_construction import (
    INGREDIENT_DATA_DIR,
    INGREDIENT_WISHLIST_FILE,
    INGREDIENT_TEMPLATE_FILE,
    openai,
)
from codiet.db.database_service import DatabaseService
from codiet.models.nutrients import (
    get_missing_leaf_nutrients,
    nutrient_is_populated,
)
from codiet.models.flags import get_missing_flags


def push_flags_to_db(flags: list[str], db_service: DatabaseService):
    """Push flags out of flag definition file into database."""
    # Add each flag to the database
    for flag in flags:
        db_service.insert_global_flag(flag)


def push_nutrients_to_db(nutrient_data: dict, db_service: DatabaseService):
    """Populate the database with nutrient data."""

    # Define a recursive function to insert either a leaf or a group nutrient
    def insert_nutrients(data, parent_id=None):
        for name, details in data.items():
            # Check if the current item is a group (has children) or a leaf (no children)
            if details["children"]:
                # It's a group nutrient, insert it using the group nutrient method
                # This method returns a unique ID which will be used as the parent ID for its children
                new_parent_id = db_service.insert_global_group_nutrient(name, parent_id)
                # Recursively insert the children
                insert_nutrients(details["children"], new_parent_id)
            else:
                # It's a leaf nutrient, insert it using the leaf nutrient method
                db_service.insert_global_leaf_nutrient(name, parent_id)

    # Call the recursive function
    insert_nutrients(nutrient_data)


def erase_all_ingredient_cost_data():
    """Remove all cost data from the ingredient .json files."""
    print("Erasing all ingredient cost data...")
    for file in os.listdir(INGREDIENT_DATA_DIR):
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)
        data["cost"]["cost_value"] = None
        data["cost"]["qty_value"] = None
        with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
            json.dump(data, f, indent=4)

def erase_all_flag_data():
    """Remove all flag data from the ingredient .json files."""
    print("Erasing all flag data...")
    for file in os.listdir(INGREDIENT_DATA_DIR):
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)
        data["flags"] = {}
        with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
            json.dump(data, f, indent=4)

def erase_all_gi_data():
    """Remove all GI data from the ingredient .json files."""
    print("Erasing all GI data...")
    for file in os.listdir(INGREDIENT_DATA_DIR):
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)
        data["GI"] = None
        with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
            json.dump(data, f, indent=4)

def title_case_ingredient_names():
    """Title case the names of all ingredient .json files."""
    print("Title casing all ingredient names...")
    for file in os.listdir(INGREDIENT_DATA_DIR):
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)
        data["name"] = data["name"].title()
        with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
            json.dump(data, f, indent=4)

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

        # Add the GI
        ingredient.gi = data["GI"]

        # Add the nutrients
        ingredient.nutrients = data["nutrients"]

        # Save the ingredient
        db_service.insert_new_ingredient(ingredient)


def remove_redundant_flags_from_datafiles(global_flags: list[str]):
    """Cycles through each ingredient file and checks it has the correct fields."""
    print("Checking for redundant flags...")
    # For each ingredient file in the directory
    for file in os.listdir(INGREDIENT_DATA_DIR):
        # Open the file and load the data
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)

        # Take a copy of all of the keys in data["flags"]
        file_flags = list(data["flags"].keys())
        for flag in file_flags:
            # Delete the flag from the datafile if it doesn't exist in the database
            if flag not in global_flags:
                del data["flags"][flag]
                print(f"Deleting flag {flag} from {file}")

        # Write the updated data back to the file
        with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
            json.dump(data, f, indent=4)


def remove_redundant_nutrients_from_datafiles(db_service: DatabaseService):
    """Cycles through each ingredient file and removes any redundant leaf nutrients.
    IMPORTANT: Only leaf nutrients are stored in the ingredient datafiles. All group
    nutrient data is calculated from the leaf nutrient data.
    """
    print("Checking for redundant leaf nutrients...")
    # Grab the leaf nutrients from the database
    global_leaf_nutrients = db_service.fetch_all_leaf_nutrient_names()
    # For each ingredient file in the directory
    for file in os.listdir(INGREDIENT_DATA_DIR):
        # Open the file and load the data
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)

        # Take a copy of all of the keys in data["nutrients"]
        file_nutrients = list(data["nutrients"].keys())
        # Cycle through all of the leaf nutrients in the file
        for nutrient in file_nutrients:
            # Delete the nutrient from the datafile if it doesn't exist in the global list
            if nutrient not in global_leaf_nutrients:
                del data["nutrients"][nutrient]
                print(f"Deleting nutrient {nutrient} from {file}")

        # Write the updated data back to the file
        with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
            json.dump(data, f, indent=4)


def init_ingredient_datafiles():
    """Work through the wishlist and initialise a corresponding ingredient .json file."""

    # Read the ingredient_wishlist.json file
    with open(INGREDIENT_WISHLIST_FILE) as f:
        wishlist = json.load(f)

    # Read the ingredient template file
    with open(INGREDIENT_TEMPLATE_FILE) as f:
        template = json.load(f)

    # For each ingredient in the wishlist
    for ingredient in wishlist:
        # Create the ingredient file name from the ingredient name
        file_name = ingredient.replace(" ", "_").lower() + ".json"

        # If the file already exists, skip it
        if any(
            file_name.lower() == existing_file.lower()
            for existing_file in os.listdir(INGREDIENT_DATA_DIR)
        ):
            print(f"Skipping {ingredient} as it already exists.")
            # Remove the ingredient from the wishlist
            wishlist.remove(ingredient)
            # Write the updated wishlist back to the file
            with open(INGREDIENT_WISHLIST_FILE, "w") as f:
                json.dump(wishlist, f)            
            continue

        # Create a .json file with this name
        with open(os.path.join(INGREDIENT_DATA_DIR, file_name), "w") as f:
            # Make a copy of the entire template
            template = template.copy()

            # Set the name of the ingredient
            template["name"] = ingredient.title()

            # Write the template data to the file
            json.dump(template, f, indent=4)

        # Remove the ingredient from the wishlist
        wishlist.remove(ingredient)
        # Write the updated wishlist back to the file
        with open(INGREDIENT_WISHLIST_FILE, "w") as f:
            json.dump(wishlist, f)


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
            description = openai._get_openai_ingredient_description(ingredient_name)
            # Write the description back to the file
            data["description"] = description

            # Save the updated data back to the file
            with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
                json.dump(data, f, indent=4)

        # If the cost data isn't filled
        if (
            data["cost"].get("cost_value") is None
            or data["cost"].get("qty_value") is None
        ):
            # Use the openai API to get the cost data
            cost_data = openai.get_openai_ingredient_cost(ingredient_name, data["cost"])

            # Write the cost data back to the file
            data["cost"] = cost_data

            # Save the updated data back to the file
            with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
                json.dump(data, f, indent=4)

        # While there are flags missing from the data
        while len(get_missing_flags(data["flags"].keys(), db_service)) > 0:
            # Use the openai API to get the flags
            flags_data = openai.get_openai_ingredient_flags(
                ingredient_name, get_missing_flags(data["flags"], db_service)
            )
            # Add the flags_data into the data["flags"] dict
            data["flags"].update(flags_data)
            # Save the updated data back to the file
            with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
                json.dump(data, f, indent=4)

        # If the GI data isn't filled, use the openai API to get the GI data
        if data.get("GI") is None:
            gi = openai.get_openai_ingredient_gi(ingredient_name)

            # Write the GI data back to the file
            data["GI"] = gi

            # Save the updated data back to the file
            with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
                json.dump(data, f, indent=4)

        # Get a list of all unpopulated nutrients
        nutrients_to_populate = []
        # Add any missing leaf nutrients
        missing_leaf_nutrients = get_missing_leaf_nutrients(data["nutrients"].keys(), db_service)
        for nutrient_name in missing_leaf_nutrients:
            nutrients_to_populate.append(nutrient_name)
        # Add any incomplete nutrients from the original dict
        for nutrient_name in data["nutrients"]:
            if not nutrient_is_populated(data["nutrients"][nutrient_name]):
                nutrients_to_populate.append(nutrient_name)
        # If we found some nutrients to populate
        if len(nutrients_to_populate) > 0:
            # Split this list into chunks not longer than 10 items
            nutrients_chunks = [
                nutrients_to_populate[i : i + 10]
                for i in range(0, len(nutrients_to_populate), 10)
            ]
            # Cycle through each chunk and populate the nutrient data
            for chunk in nutrients_chunks:
                # Use the openai API to get the nutrient data
                nutrient_data = openai.get_openai_ingredient_nutrients(
                    ingredient_name, chunk
                )
                # Add the nutrient_data into the data["nutrients"] dict
                data["nutrients"].update(nutrient_data)

            # Save the updated data back to the file
            with open(os.path.join(INGREDIENT_DATA_DIR, file), "w") as f:
                json.dump(data, f, indent=4)

        # Now update some special nutrient cases based on the flags
        # If the alcohol free flag is present, set the alcohol nutrient to 0
        if "alcohol free" in data["flags"]:
            data["nutrients"]["alcohol"]["nutr_qty_value"] = 0
        # If lactose free flag is present, set the lactose nutrient to 0
        if "lactose free" in data["flags"]:
            data["nutrients"]["lactose"]["nutr_qty_value"] = 0

        # # If the cost data references a volume, calculate the density
        # if data["cost"]["qty_unit"] in ["ml"]:
        #     # Calculate the density
        #     density = data["cost"]["cost_value"] / data["cost"]["qty_value"]
        #     # Update the density data in the file
        #     data["bulk"]["density"]["mass_unit"] = "g
"""Module of utility functions for collating and correcting the raw datafiles
used to populate the database."""

import os, json
from typing import Callable

from codiet.db_construction import openai

from codiet.db_construction import (
    FLAG_DATA_FILEPATH,
    NUTRIENT_DATA_FILEPATH,
    INGREDIENT_DATA_DIR,
    INGREDIENT_WISHLIST_FILEPATH,
    INGREDIENT_TEMPLATE_FILEPATH,
)
from codiet.utils.nutrients import find_leaf_nutrients, get_missing_leaf_nutrient_names
from codiet.utils.flags import get_missing_flags

# Define some data caches to avoid reloading the same data multiple times
_cached_ingredient_template: dict | None = None
_cached_global_flags: dict | None = None
_cached_nutrient_data_template: dict | None = None
_cached_leaf_nutrient_names: list[str] | None = None

def apply_to_each_ingredient_datafile(callback: Callable[[dict], None]) -> None:
    """Loads each ingredient datafile, runs the callback, and writes the data back."""
    # For each ingredient file in the directory
    for ingredient_filename in os.listdir(INGREDIENT_DATA_DIR):
        # Build its filepath
        ingredient_filepath = os.path.join(INGREDIENT_DATA_DIR, ingredient_filename)
        # Load the ingredient data from the file
        with open(ingredient_filepath) as file:
            ingredient_data = json.load(file)
        # Run the callback, passing in the data
        callback(ingredient_data)
        # Write the updated data back to the file
        with open(ingredient_filepath, "w") as file:
            json.dump(ingredient_data, file, indent=4)
# Create an alias
for_all_ingredients = apply_to_each_ingredient_datafile


def get_ingredient_template() -> dict:
    """Return the ingredient template data from cache."""
    # Use the global variable, don't create a new one
    global _cached_ingredient_template
    # If the template has not been loaded yet
    if _cached_ingredient_template is None:
        # Load it from the file and cache it
        with open(INGREDIENT_TEMPLATE_FILEPATH) as ingredient_template_file:
            _cached_ingredient_template = json.load(ingredient_template_file)
    # Return the cached template
    return _cached_ingredient_template  # type: ignore

def get_global_flag_names() -> list[str]:
    """Return the global flags data from cache."""
    # Use the global variable, don't create a new one
    global _cached_global_flags
    # If the flags have not been loaded yet
    if _cached_global_flags is None:
        # Load it from the file and cache it
        with open(FLAG_DATA_FILEPATH) as global_flags_file:
            _cached_global_flags = json.load(global_flags_file)
    # Return the cached flags
    return _cached_global_flags  # type: ignore

def get_nutrient_data_template() -> dict:
    """Return the nutrient data from cache."""
    # Use the global variable, don't create a new one
    global _cached_nutrient_data_template
    # If the nutrient data has not been loaded yet
    if _cached_nutrient_data_template is None:
        # Load it from the file and cache it
        with open(NUTRIENT_DATA_FILEPATH) as nutrient_data_file:
            _cached_nutrient_data_template = json.load(nutrient_data_file)
    # Return the cached nutrient data
    return _cached_nutrient_data_template  # type: ignore

def get_leaf_nutrient_names() -> list[str]:
    """Return the leaf nutrient names from cache."""
    # Use the global variable, don't create a new one
    global _cached_leaf_nutrient_names
    # If the leaf nutrient names have not been loaded yet
    if _cached_leaf_nutrient_names is None:
        # Load it from the file and cache it
        with open(NUTRIENT_DATA_FILEPATH) as nutrient_data_file:
            nutrient_data = json.load(nutrient_data_file)
            _cached_leaf_nutrient_names = find_leaf_nutrients(nutrient_data)
    # Return the cached leaf nutrient names
    return _cached_leaf_nutrient_names  # type: ignore

def erase_ingredient_cost_data(ingredient_data:dict) -> None:
    """Remove the cost data from an ingredient .json file."""
    # Update the console
    print(f"Erasing cost data from {ingredient_data['name']}...")
    # Reset the cost data to the template
    ingredient_data["cost"] = get_ingredient_template()["cost"]

def erase_ingredient_density_data(ingredient_data:dict) -> None:
    """Remove the density data from an ingredient .json file."""
    # Update the console
    print(f"Erasing density data from {ingredient_data['name']}...")
    # Reset the density data to the template
    ingredient_data["bulk"]["density"] = get_ingredient_template()["bulk"][
        "density"
    ]

def erase_ingredient_flag_data(ingredient_data:dict) -> None:
    """Remove all flag data from the ingredient .json file."""
    # Update the console
    print(f"Erasing flags from {ingredient_data['name']}...")
    # Reset the flag data to an empty dict
    ingredient_data["flags"] = get_ingredient_template()["flags"]

def erase_ingredient_gi_data(ingredient_data:dict) -> None:
    """Remove all GI data from the ingredient .json file."""
    # Update the console
    print(f"Erasing GI data from {ingredient_data['name']}...")
    # Reset the GI data to None
    ingredient_data["GI"] = get_ingredient_template()["GI"]

def erase_ingredient_nutrient_data(ingredient_data:dict) -> None:
    """Remove all nutrient data from the ingredient .json file."""
    # Update the console
    print(f"Erasing nutrient data from {ingredient_data['name']}...")
    # Reset the nutrient data to an empty dict
    ingredient_data["nutrients"] = get_ingredient_template()["nutrients"]

def title_case_ingredient_name(ingredient_data: dict) -> None:
    """Title case the ingredient name in the .json file."""
    # Update the console
    print(f"Title casing {ingredient_data['name']}...")
    # Title case the name of the ingredient
    ingredient_data["name"] = ingredient_data["name"].title()

def remove_redundant_flags_from_datafile(ingredient_data: dict) -> None:
    """Removes any redundant flags from the ingredient data."""
    # Update the console
    print(f"Checking for redundant flags in {ingredient_data['name']}...")
    # Take a copy of all of the keys in data["flags"]
    ingredient_flags = list(ingredient_data["flags"].keys())
    for flag in ingredient_flags:
        # Delete the flag from the datafile if it doesn't exist in the database
        if flag not in get_global_flag_names():
            print(f"Deleting flag {flag} from {ingredient_data["name"]}")
            del ingredient_data["flags"][flag]

def remove_redundant_nutrients_from_ingredient_datafile(ingredient_data: dict) -> None:
    """Removes any redundant leaf nutrients from the ingredient data.
    IMPORTANT: Only leaf nutrients are stored in the ingredient datafiles. All group
    nutrient data is calculated from the leaf nutrient data.
    """
    # Update the console
    print(f"Checking for redundant nutrients in {ingredient_data['name']}...")
    # Take a copy of all of the nutrient names in the ingredient's nutrient data
    ingredient_nutrient_names = list(ingredient_data["nutrients"].keys())
    # Cycle through all of the leaf nutrients in the file
    for ingredient_nutrient_name in ingredient_nutrient_names:
        # Delete the nutrient from the datafile if it doesn't exist in the global list
        if ingredient_nutrient_name not in get_leaf_nutrient_names():
            print(f"Deleting nutrient {ingredient_nutrient_name} from {ingredient_data["name"]}")
            del ingredient_data["nutrients"][ingredient_nutrient_name]

def ingredient_datafile_exists(ingredient_datafile_name: str) -> bool:
    """Check if an ingredient datafile exists."""
    return os.path.isfile(os.path.join(INGREDIENT_DATA_DIR, ingredient_datafile_name))

def remove_ingredient_from_wishlist(ingredient_name: str):
    """Remove an ingredient from the wishlist."""
    # Read the ingredient_wishlist.json file
    with open(INGREDIENT_WISHLIST_FILEPATH) as f:
        ingredient_wishlist = json.load(f)
    # Remove the ingredient from the wishlist
    ingredient_wishlist.remove(ingredient_name)
    # Write the updated wishlist back to the file
    with open(INGREDIENT_WISHLIST_FILEPATH, "w") as f:
        json.dump(ingredient_wishlist, f, indent=4)

def insert_new_ingredient_datafile_from_template(ingredient_name: str):
    """Create a new ingredient datafile from the template."""
    # Load the ingredient template
    ingredient_template = get_ingredient_template()
    # Update the name of the ingredient in the template
    ingredient_template["name"] = ingredient_name
    # Create the ingredient file name from the ingredient name
    ingredient_datafile_name = ingredient_name.replace(" ", "_").lower() + ".json"
    # Write the template to the new ingredient file
    with open(os.path.join(INGREDIENT_DATA_DIR, ingredient_datafile_name), "w") as f:
        json.dump(ingredient_template, f, indent=4)

def init_ingredient_datafiles():
    """Work through the wishlist and initialise a corresponding ingredient .json file."""
    # Read the ingredient_wishlist.json file
    with open(INGREDIENT_WISHLIST_FILEPATH) as f:
        ingredient_wishlist = json.load(f)
    # For each ingredient in the wishlist
    for ingredient_name in ingredient_wishlist:
        # Create the ingredient file name from the ingredient name
        ingredient_datafile_name = ingredient_name.replace(" ", "_").lower() + ".json"
        # If the file already exists, skip it
        if ingredient_datafile_exists(ingredient_datafile_name):
            # Update the console
            print(f"Skipping {ingredient_name} as it already exists.")
            # Remove the ingredient from the wishlist
            remove_ingredient_from_wishlist(ingredient_name)
            continue
        else:
            # Update the console
            print(f"Creating {ingredient_datafile_name}...")
            # Create the ingredient file from the template
            insert_new_ingredient_datafile_from_template(ingredient_name)
            # Remove the ingredient from the wishlist
            remove_ingredient_from_wishlist(ingredient_name)


def populate_ingredient_datafiles():
    """Module for handling ingredient files in the ingredients data directory.

    This module processes each ingredient file in the ingredients data directory
    and populates its data using the OpenAI API. 

    Note:
        The file is written back every time the OpenAI API is used. This is to 
        prevent data loss. The various sections are also populated in a specific
        order, to enable some data to be used in the population of other data.
        For example, if the flags are done before nutrients, the flags can be used
        to imply certain nutrient values.
    """
    # Update the console
    print("Populating ingredient datafiles...")
    # Populate the datafiles
    for_all_ingredients(populate_ingredient_datafile_description)
    for_all_ingredients(populate_ingredient_datafile_cost)
    for_all_ingredients(populate_ingredient_datafile_flags)
    for_all_ingredients(populate_ingredient_datafile_gi)
    for_all_ingredients(populate_ingredient_datafile_nutrients)
    for_all_ingredients(populate_ingredient_datafile_density)


def populate_ingredient_datafile_description(ingredient_data: dict) -> None:
    """Populates the description in the ingredient datafile."""
    # Update the console
    print(f"Populating description in {ingredient_data['name']}...")
    # Grab the ingredient name
    ingredient_name = ingredient_data["name"]
    # If the description isn't filled
    if ingredient_data.get("description") is None:
        # Update the terminal
        print(f"Getting description for {ingredient_name}...")
        # Use the openai API to get the description
        description = openai.get_openai_ingredient_description(ingredient_name)
        # Write the description back to the file
        ingredient_data["description"] = description


def populate_ingredient_datafile_cost(ingredient_data: dict) -> None:
    """Populate the cost data in the ingredient datafile."""
    # Update the console
    print(f"Populating cost in {ingredient_data['name']}...")
    # Grab the ingredient name
    ingredient_name = ingredient_data["name"]
    # Update the console
    print(f"Getting cost for {ingredient_name}...")
    # If the cost data isn't filled
    if (
        ingredient_data["cost"].get("cost_value") is None
        or ingredient_data["cost"].get("qty_value") is None
    ):
        # Use the openai API to get the cost data
        cost_data = openai.get_openai_ingredient_cost(
            ingredient_name, ingredient_data["cost"]
        )
        # Write the cost data back to the file
        ingredient_data["cost"] = cost_data

def populate_ingredient_datafile_flags(ingredient_data: dict) -> None:
    """Populate the flags in the ingredient datafile."""
    # Update the console
    print(f"Populating flags in {ingredient_data['name']}...")
    # Grab the ingredient name
    ingredient_name = ingredient_data["name"]
    # Get a list of any missing flags
    missing_flag_names = get_missing_flags(ingredient_data["flags"].keys(), get_global_flag_names())
    # If we are missing some flags
    if len(missing_flag_names) > 0:
        # Update the console
        print(f"Getting flags for {ingredient_name}...")
        # Use the openai API to get the flags
        flags_data = openai.get_openai_ingredient_flags(ingredient_name, missing_flag_names)
        # Add the flags_data into the data["flags"] dict
        ingredient_data["flags"].update(flags_data)

def populate_ingredient_datafile_gi(ingredient_data: dict) -> None:
    """Populate the GI data in the ingredient datafile."""
    # Grab the ingredient name
    ingredient_name = ingredient_data["name"]
    # If the GI data isn't filled
    if ingredient_data.get("GI") is None:
        # Use the openai API to get the GI data
        gi = openai.get_openai_ingredient_gi(ingredient_name)
        # Write the GI data back to the file
        ingredient_data["GI"] = gi

def populate_ingredient_datafile_nutrients(ingredient_data: dict) -> None:
    """Populate the nutrient data of the ingredient datafile."""
    # Grab the ingredient name
    ingredient_name = ingredient_data["name"]
    # Get a list of all unpopulated nutrients
    nutrients_to_populate = get_missing_leaf_nutrient_names(
        nutrient_names=ingredient_data["nutrients"].keys(),
        global_leaf_nutrient_names=get_leaf_nutrient_names(),
    )
    # If we found some nutrients to populate
    if len(nutrients_to_populate) > 0:
        # Split this list into chunks not longer than 5 items
        # or GPT seems to get lazy and not return all the data.
        chunk_length = 5
        nutrients_chunks = [
            nutrients_to_populate[i : i + chunk_length]
            for i in range(0, len(nutrients_to_populate), chunk_length)
        ]
        # Cycle through each chunk and populate the nutrient data
        for chunk in nutrients_chunks:
            # Use the openai API to get the nutrient data
            nutrient_data = openai.get_openai_ingredient_nutrients(
                ingredient_name, chunk
            )
            # Add the nutrient_data into the data["nutrients"] dict
            ingredient_data["nutrients"].update(nutrient_data)
    # Now update some special nutrient cases based on the flags
    # If the alcohol free flag is present, set the alcohol nutrient to 0
    if "alcohol free" in ingredient_data["flags"]:
        ingredient_data["nutrients"]["alcohol"]["nutr_qty_value"] = 0
    # If lactose free flag is present, set the lactose nutrient to 0
    if "lactose free" in ingredient_data["flags"]:
        ingredient_data["nutrients"]["lactose"]["nutr_qty_value"] = 0

def _density_data_is_populated(ingredient_data: dict) -> bool:
    """Check if the density data is populated."""
    return (
        ingredient_data["bulk"]["density"]["mass_value"] is not None
        and ingredient_data["bulk"]["density"]["vol_value"] is not None
    )

def _density_data_is_required(ingredient_data: dict) -> bool:
    """Check if the density data is required."""
    # Do any of the nutrients or cost have a volume unit?
    volumes_used = False
    if ingredient_data["cost"]["qty_unit"] in ["ml, L"]:
        volumes_used = True
    for nutrient in ingredient_data["nutrients"]:
        if ingredient_data["nutrients"][nutrient]["ing_qty_unit"] in ["ml, L"]:
            volumes_used = True
    return volumes_used

def populate_ingredient_datafile_density(ingredient_data: dict) -> None:
    """Populate the density data of the ingredient datafiles."""
    # Grab the ingredient name
    ingredient_name = ingredient_data["name"]
    # If the density data isn't filled and is required
    if not _density_data_is_populated and _density_data_is_required:
        # Use the openai API to get the density data
        density_data = openai.get_openai_ingredient_density(ingredient_name)
        # Write the density data back to the file
        ingredient_data["bulk"]["density"] = density_data

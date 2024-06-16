"""Module of utility functions for collating and correcting the raw datafiles
used to populate the database."""

import os, json
from copy import deepcopy
from typing import Callable

from codiet.db_population import openai

from codiet.db_population import (
    GLOBAL_FLAG_DATA_FILEPATH,
    GLOBAL_NUTRIENT_DATA_FILEPATH,
    INGREDIENT_DATA_DIR,
    INGREDIENT_TEMPLATE_FILEPATH,
    INGREDIENT_COST_TEMPLATE_FILEPATH,
    INGREDIENT_CUSTOM_UNITS_TEMPLATE_FILEPATH,
    INGREDIENT_NUTRIENT_QUANTITY_TEMPLATE_FILEPATH
)
from codiet.utils.dict import align_keys_with_template
from codiet.utils.strings import string_is_populated, convert_snake_case_to_title_case
from codiet.utils.numbers import value_is_positive_number
from codiet.utils.nutrients import find_leaf_nutrients, get_missing_leaf_nutrient_names
from codiet.utils.flags import get_missing_flags

# Define some data caches to avoid reloading the same data multiple times
_cached_ingredient_template: dict | None = None
_cached_cost_data_template: dict | None = None
_cached_custom_units_data_template: dict | None = None
_cached_global_flags: dict | None = None
_cached_flag_data_template: dict[str, bool] | None = None
_cached_nutrient_data_template: dict | None = None
_cached_leaf_nutrient_names: list[str] | None = None
_cached_nutrient_quantity_data_template: dict | None = None

def apply_to_each_ingredient_datafile(callback: Callable[[str, dict], None]) -> None:
    """Loads each ingredient datafile, runs the callback, and writes the data back."""
    # Work through each datafile in the ingredient directory
    for ingredient_filename in os.listdir(INGREDIENT_DATA_DIR):
        # Build its filepath
        ingredient_filepath = os.path.join(INGREDIENT_DATA_DIR, ingredient_filename)
        # Load the ingredient data from the file
        with open(ingredient_filepath) as file:
            ingredient_data = json.load(file)
        # Take a copy of the original
        original_ingredient_data = deepcopy(ingredient_data)
        # Run the callback, passing in the data
        callback(ingredient_filename, ingredient_data)
        # If the data has changed
        if ingredient_data != original_ingredient_data:
            print(f"Updating {ingredient_filename}")
            # Write the updated data back to the file
            with open(ingredient_filepath, "w") as file:
                json.dump(ingredient_data, file, indent=4)
# Create an alias
for_all_ingredients = apply_to_each_ingredient_datafile

def autocomplete_ingredient_datafile(filename, ingredient_data: dict) -> None:
    """Populates the data in an ingredient .json file."""
    autocomplete_ingredient_name(filename, ingredient_data)
    autocomplete_ingredient_datafile_custom_units(ingredient_data)
    autocomplete_ingredient_datafile_description(ingredient_data)
    autocomplete_ingredient_datafile_cost(ingredient_data)
    # autocomplete_ingredient_datafile_flags(ingredient_data)
    # autocomplete_ingredient_datafile_gi(ingredient_data)
    # autocomplete_ingredient_datafile_nutrients(ingredient_data)

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

def ingredient_datafile_exists(ingredient_datafile_name: str) -> bool:
    """Check if an ingredient datafile exists."""
    return os.path.isfile(os.path.join(INGREDIENT_DATA_DIR, ingredient_datafile_name))

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

def align_top_level_fields_with_template(filename:str, ingredient_data: dict) -> None:
    """Removes any redundant top level fields from the ingredient data."""
    # Grab the ingredient template
    ingredient_template = get_ingredient_template()
    # Align the top level fields with the template
    align_keys_with_template(ingredient_template, ingredient_data)

def autocomplete_ingredient_name(filename:str, ingredient_data:dict) -> None:
    """Remove the name data from an ingredient .json file."""
    if not string_is_populated(ingredient_data["name"]):
        # Remove the extension from the filename if present
        # Split on the dot and discard the last element
        filename = filename.split(".")[0]
        # Reset the name data to an empty string
        print(f"Autocompleting name for {filename}")
        ingredient_data["name"] = convert_snake_case_to_title_case(filename)

def reset_ingredient_description_data(filename:str, ingredient_data:dict) -> None:
    """Remove the description data from an ingredient .json file."""
    # Reset the description data to an empty string
    ingredient_data["description"] = ""

def description_is_populated(ingredient_data: dict) -> bool:
    """Check if the description is populated in the ingredient datafile."""
    return string_is_populated(ingredient_data["description"])

def autocomplete_ingredient_datafile_description(ingredient_data: dict) -> None:
    """Populates the description in the ingredient datafile."""
    # Grab the ingredient name
    ingredient_name = ingredient_data["name"]
    # If the description data isn't filled
    if description_is_populated(ingredient_data) is False:
        # Use the openai API to get the description
        description = openai.get_openai_ingredient_description(ingredient_name)
        # Write the description back to the file
        ingredient_data["description"] = description

def get_ingredient_cost_data_template() -> dict:
    """Return the ingredient cost data from cache."""
    global _cached_cost_data_template
    if _cached_cost_data_template is None:
        with open(INGREDIENT_COST_TEMPLATE_FILEPATH) as f:
            _cached_cost_data_template = json.load(f)    
    return _cached_cost_data_template  # type: ignore

def cost_data_is_populated(ingredient_data: dict) -> bool:
    """Check if the cost data is populated in the ingredient datafile."""
    return (
        ingredient_data["cost"].get("cost_value") is not None
        and ingredient_data["cost"].get("qty_value") is not None
    )

def autocomplete_ingredient_datafile_cost(ingredient_data: dict) -> None:
    """Populate the cost data in the ingredient datafile."""
    if cost_data_is_populated(ingredient_data) is False:
        # Use the openai API to get the cost data
        cost_data = openai.get_openai_ingredient_cost(
            ingredient_data["name"], ingredient_data["cost"]
        )
        # Write the cost data back to the file
        ingredient_data["cost"] = cost_data

def align_cost_data_with_template(filename:str, ingredient_data:dict) -> None:
    """Remove any malformed cost data from the ingredient .json file."""
    # Grab the cost data template
    cost_data_template = get_ingredient_cost_data_template()
    # Align the cost data with the template
    align_keys_with_template(cost_data_template, ingredient_data["cost"])

def get_ingredient_custom_units_data_template() -> dict:
    """Return the ingredient custom units data from cache."""
    global _cached_custom_units_data_template
    if _cached_custom_units_data_template is None:
        with open(INGREDIENT_CUSTOM_UNITS_TEMPLATE_FILEPATH) as f:
            _cached_custom_units_data_template = json.load(f)
    return _cached_custom_units_data_template  # type: ignore

def reset_ingredient_custom_unit_data(filename:str, ingredient_data:dict) -> None:
    """Remove all custom unit data from the ingredient .json file."""
    # Reset the custom unit data to an empty list
    ingredient_data["custom_units"] = {}

def align_custom_units_data_with_template(filename:str, ingredient_data:dict) -> None:
    """Remove any malformed custom units data from the ingredient .json file."""
    # Grab the custom unit data template
    custom_units_data_template = get_ingredient_template()["custom_units"]
    # For each custom unit field in the ingredient data
    for custom_unit_data in ingredient_data["custom_units"]:
        # Align the custom unit data with the template
        align_keys_with_template(custom_units_data_template, custom_unit_data)

def autocomplete_ingredient_datafile_custom_units(ingredient_data: dict) -> None:
    """Populate the custom units in the ingredient datafile."""
    raise NotImplementedError("This function is not yet implemented.")

def reset_ingredient_cost_data(filename:str, ingredient_data:dict) -> None:
    """Remove the cost data from an ingredient .json file."""
    # Reset the cost data to the template
    ingredient_data["cost"] = get_ingredient_cost_data_template()

def get_global_flag_names() -> list[str]:
    """Return the global flags data from cache."""
    # Use the global variable, don't create a new one
    global _cached_global_flags
    # If the flags have not been loaded yet
    if _cached_global_flags is None:
        # Load it from the file and cache it
        with open(GLOBAL_FLAG_DATA_FILEPATH) as global_flags_file:
            _cached_global_flags = json.load(global_flags_file)
    # Return the cached flags
    return _cached_global_flags  # type: ignore

def get_flag_data_template() -> dict:
    """Return the flag data from cache."""
    global _cached_flag_data_template
    if _cached_flag_data_template is None:
        # Grab the flag list first
        flag_names = get_global_flag_names()
        # Create a dict with all flags set to False
        _cached_flag_data_template = {flag_name: False for flag_name in flag_names}
    return _cached_flag_data_template  # type: ignore

def remove_redundant_flags_from_datafile(filename:str, ingredient_data: dict) -> None:
    """Removes any redundant flags from the ingredient data."""
    # Take a copy of all of the keys in data["flags"]
    ingredient_flags = list(ingredient_data["flags"].keys())
    for flag in ingredient_flags:
        # Delete the flag from the datafile if it doesn't exist in the database
        if flag not in get_global_flag_names():
            print(f"Deleting flag {flag} from {ingredient_data["name"]}")
            del ingredient_data["flags"][flag]

def reset_ingredient_flag_data(filename:str, ingredient_data:dict) -> None:
    """Remove all flag data from the ingredient .json file."""
    # Reset the flag data to an empty dict
    ingredient_data["flags"] = get_flag_data_template()

def autocomplete_ingredient_datafile_flags(ingredient_data: dict) -> None:
    """Populate the flags in the ingredient datafile."""
    # Get a list of any missing flags
    missing_flag_names = get_missing_flags(list(ingredient_data["flags"].keys()), get_global_flag_names())
    # If we are missing some flags
    if len(missing_flag_names) > 0:
        # Use the openai API to get the flags
        flags_data = openai.get_openai_ingredient_flags(ingredient_data["name"], missing_flag_names)
        # Add the flags_data into the data["flags"] dict
        ingredient_data["flags"].update(flags_data)

def reset_ingredient_gi_data(filename:str, ingredient_data:dict) -> None:
    """Remove all GI data from the ingredient .json file."""
    # Reset the GI data to None
    ingredient_data["GI"] = None

def gi_is_populated(ingredient_data: dict) -> bool:
    """Check if the GI data is populated in the ingredient datafile."""
    return ingredient_data.get("GI") is not None and ingredient_data["GI"].strip() != ""

def autocomplete_ingredient_datafile_gi(ingredient_data: dict) -> None:
    """Populate the GI data in the ingredient datafile."""
    # Grab the ingredient name
    ingredient_name = ingredient_data["name"]
    # If the GI data isn't filled
    if gi_is_populated(ingredient_data) is False:
        # Use the openai API to get the GI data
        gi = openai.get_openai_ingredient_gi(ingredient_name)
        # Write the GI data back to the file
        ingredient_data["GI"] = gi
    # TODO: Add a method to check that if there is no carbohydrate, the GI is set to None.

def get_global_nutrient_data() -> dict:
    """Return the nutrient data from cache."""
    # Use the global variable, don't create a new one
    global _cached_nutrient_data_template
    # If the nutrient data has not been loaded yet
    if _cached_nutrient_data_template is None:
        # Load it from the file and cache it
        with open(GLOBAL_NUTRIENT_DATA_FILEPATH) as nutrient_data_file:
            _cached_nutrient_data_template = json.load(nutrient_data_file)
    # Return the cached nutrient data
    return _cached_nutrient_data_template  # type: ignore

def get_leaf_nutrient_names() -> list[str]:
    """Return the leaf nutrient names from cache."""
    # Use the global variable, don't create a new one
    global _cached_leaf_nutrient_names
    # If the leaf nutrient names have not been loaded yet
    if _cached_leaf_nutrient_names is None:
        # Build it and cache it
        nutrient_data = get_global_nutrient_data()
        _cached_leaf_nutrient_names = find_leaf_nutrients(nutrient_data)
    # Return the cached leaf nutrient names
    return _cached_leaf_nutrient_names  # type: ignore

def get_nutrient_quantity_data_template() -> dict:
    """Return the nutrient quantity data from cache."""
    global _cached_nutrient_quantity_data_template
    if _cached_nutrient_quantity_data_template is None:
        with open(INGREDIENT_NUTRIENT_QUANTITY_TEMPLATE_FILEPATH) as f:
            _cached_nutrient_quantity_data_template = json.load(f)
    return _cached_nutrient_quantity_data_template  # type: ignore

def reset_ingredient_nutrient_data(filename:str, ingredient_data:dict) -> None:
    """Remove all nutrient data from the ingredient .json file."""
    # Init the nutrients dict
    ingredient_data["nutrients"] = {}
    # For each leaf nutrient
    for leaf_nutrient_name in get_leaf_nutrient_names():
        # Reset the nutrient data to the template
        ingredient_data["nutrients"][leaf_nutrient_name] = get_nutrient_quantity_data_template()

def align_nutrient_quantity_data_with_template(filename:str, ingredient_data:dict) -> None:
    """Remove any malformed nutrient quantity data from the ingredient .json file."""
    # Grab the nutrient data template
    nutrient_data_template = get_nutrient_quantity_data_template()
    # For each nutrient in the ingredient data
    for nutrient_data in ingredient_data["nutrients"].values():
        # Align the nutrient quantity data with the template
        align_keys_with_template(nutrient_data_template, nutrient_data)

def remove_redundant_nutrients_from_datafile(filename:str, ingredient_data: dict) -> None:
    """Removes any redundant leaf nutrients from the ingredient data.
    IMPORTANT: Only leaf nutrients are stored in the ingredient datafiles. All group
    nutrient data is calculated from the leaf nutrient data.
    """
    # Take a copy of all of the nutrient names in the ingredient's nutrient data
    ingredient_nutrient_names = list(ingredient_data["nutrients"].keys())
    # Cycle through all of the leaf nutrients in the file
    for ingredient_nutrient_name in ingredient_nutrient_names:
        # Delete the nutrient from the datafile if it doesn't exist in the global list
        if ingredient_nutrient_name not in get_leaf_nutrient_names():
            print(f"Deleting nutrient {ingredient_nutrient_name} from {ingredient_data["name"]}")
            del ingredient_data["nutrients"][ingredient_nutrient_name]

def nutrient_data_is_populated(nutrient_data: dict) -> bool:
    """Check if the nutrient data is populated in the ingredient datafile."""
    if string_is_populated(nutrient_data["nutr_mass_unit"]) is False:
        return False
    if value_is_positive_number(nutrient_data["nutr_mass_value"]) is False:
        return False
    if string_is_populated(nutrient_data["ing_qty_unit"]) is False:
        return False
    if value_is_positive_number(nutrient_data["ing_qty_value"]) is False:
        return False
    return True

def find_missing_or_incomplete_leaf_nutrients(ingredient_data: dict) -> list[str]:
    """Return a list of missing or incomplete leaf nutrients in the ingredient datafile."""
    # Create a list of missing or incomplete nutrients
    missing_nutrients = []
    # Grab the master leaf nutrient name
    leaf_nutrient_names = get_leaf_nutrient_names()
    # The nutrient data is under "nutrients" in the ingredient data.
    # Cycle through each leaf nutrient name and check if it is in the data
    # If it is not, add it to the missing_nutrients list
    for nutrient_name in leaf_nutrient_names:
        if nutrient_name not in ingredient_data["nutrients"]:
            missing_nutrients.append(nutrient_name)
    # Now work through each nutrient in the data and check if it is complete
    for nutrient_name, nutrient_data in ingredient_data["nutrients"].items():
        if nutrient_data_is_populated(nutrient_data) is False:
            missing_nutrients.append(nutrient_name)
    # Return the list of missing nutrients
    return missing_nutrients

def autocomplete_ingredient_datafile_nutrients(ingredient_data: dict) -> None:
    """Populate the nutrient data of the ingredient datafile."""
    # Grab the ingredient name
    ingredient_name = ingredient_data["name"]
    # Get a list of all missing or incomplete nutrients
    nutrients_to_populate = find_missing_or_incomplete_leaf_nutrients(ingredient_data)
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
        ingredient_data["nutrients"]["alcohol"]["nutr_mass_value"] = 0
    # If lactose free flag is present, set the lactose nutrient to 0
    if "lactose free" in ingredient_data["flags"]:
        ingredient_data["nutrients"]["lactose"]["nutr_mass_value"] = 0

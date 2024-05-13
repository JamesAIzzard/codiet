"""
Module to handle all data sourcing and database population.
"""

import os

from codiet.db import DB_PATH
from codiet.db_construction import ingredient_datafile_utils
from codiet.db_construction.ingredient_datafile_utils import apply_to_each_ingredient_datafile as for_all_ingredients
from codiet.db_construction import populate_database
from codiet.db_construction.create_schema import create_schema

if __name__ == '__main__':
    # Update the console
    print("Beginning database processing...")

    # DATAFILE UPDATES
    # The following four calls work together to bring all ingredient .json
    # files up to date with the current flags and nutrients.
    # Work through the existing datafiles and remove any redundant flags and nutrients
    print("Processing existing datafiles...")
    for_all_ingredients(ingredient_datafile_utils.remove_redundant_flags_from_datafile)
    for_all_ingredients(ingredient_datafile_utils.remove_redundant_nutrients_from_ingredient_datafile)
    # Make sure all existing ingredients have title case names
    for_all_ingredients(ingredient_datafile_utils.title_case_ingredient_name)
    print("Initialising new datafiles...")
    # Initialise the ingredient datafiles from the wishlist and template
    ingredient_datafile_utils.init_ingredient_datafiles()
    print("Populating missing data from ingredient datafiles...")
    # Use the OpenAI model to populate the ingredient datafiles
    ingredient_datafile_utils.populate_ingredient_datafiles()

    # DANGER ZONE: The following calls will erase all data from the database
    # print("Resetting datafile data...")
    # for_all_ingredients(datafile_utils.reset_ingredient_cost_data)
    # for_all_ingredients(datafile_utils.reset_ingredient_density_data)
    # for_all_ingredients(datafile_utils.reset_ingredient_flag_data)
    # for_all_ingredients(datafile_utils.reset_ingredient_gi_data)
    # for_all_ingredients(datafile_utils.reset_ingredient_nutrient_data)

    # DATABASE CREATION
    # Remove any database that exists
    if os.path.exists(DB_PATH):
        print(f"Removing existing database at {DB_PATH}")
        os.remove(DB_PATH)
    # Rebuild the database schema
    create_schema()

    # DATABASE POPULATION
    # Push all of the ingredient .json data into the database
    print("Pushing datafile data into database...")
    populate_database.push_flags_to_db()
    populate_database.push_nutrients_to_db()
    populate_database.push_ingredients_to_db()
    populate_database.push_global_recipe_types_to_db()
    # Push all of the recipe .json data into the database
    print("Pushing recipe data into database...")
    populate_database.push_global_recipe_types_to_db()
    populate_database.push_recipes_to_db()

    # Update the console
    print("Database processing complete.")
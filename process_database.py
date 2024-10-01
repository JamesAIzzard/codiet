"""
Top level module for data sourcing and database population.
"""
# TODO: Consider splitting into two modules, one for data sourcing
# and one for database population.

import os

from codiet.sqlite_db import DB_PATH
from codiet.sqlite_db.database import Database
from codiet.sqlite_db.repository import Repository
from codiet.sqlite_db.database_service import DatabaseService
from codiet.json_db import populate_db_from_json
from codiet.json_db.ingredients import ingredient_datafile_utils
from codiet.json_db.ingredients.ingredient_datafile_utils import apply_to_each_ingredient_datafile as for_all_ingredients

# Create the database objects
database = Database(DB_PATH)
repository = Repository(database)
db_service = DatabaseService(repository)

if __name__ == '__main__':
    # Update the console
    print("Beginning database processing...")

    # DANGER ZONE: The following calls will erase all data from the datafiles
    # print("Resetting datafile data...")
    # print("Resetting ingredient names...")
    # for_all_ingredients(ingredient_datafile_utils.reset_ingredient_name)
    # print("Resetting ingredient descriptions...")
    # for_all_ingredients(ingredient_datafile_utils.reset_ingredient_description_data)
    # print("Resetting ingredient cost data...")
    # for_all_ingredients(ingredient_datafile_utils.reset_ingredient_cost_data)
    # print("Resetting ingredient custom unit data...")
    # for_all_ingredients(ingredient_datafile_utils.reset_ingredient_custom_unit_data)
    # print("Resetting ingredient flag data...")
    # for_all_ingredients(ingredient_datafile_utils.reset_ingredient_flag_data)
    # print("Resetting ingredient GI data...")
    # for_all_ingredients(ingredient_datafile_utils.reset_ingredient_gi_data)
    # print("Resetting ingredient nutrient data...")
    # for_all_ingredients(ingredient_datafile_utils.reset_ingredient_nutrient_data)

    # DATAFILE ALIGNMENT
    # print("Processing existing datafiles...")
    # print("Aligning top level fields with template...")
    # for_all_ingredients(ingredient_datafile_utils.align_top_level_fields_with_template)
    # print("Aligning cost data with template...")
    # for_all_ingredients(ingredient_datafile_utils.align_cost_data_with_template)
    # print("Aligning custom units data with template...")
    # for_all_ingredients(ingredient_datafile_utils.align_custom_units_data_with_template)
    # print("Aligning flag data with template...")
    # for_all_ingredients(ingredient_datafile_utils.remove_redundant_flags_from_datafile)
    # print("Removing redundant nutrient quantities...")
    # for_all_ingredients(ingredient_datafile_utils.remove_redundant_nutrients_from_datafile)
    # print("Aligning nutrient quantity data with template...")
    # for_all_ingredients(ingredient_datafile_utils.align_nutrient_quantity_data_with_template)

    # # DATAFILE POPULATION
    # print("Populating missing data from ingredient datafiles...")
    # # Use the OpenAI model to populate the ingredient datafiles
    # for_all_ingredients(ingredient_datafile_utils.autocomplete_ingredient_datafile)

    # Reset the database schema
    print("Resetting database schema...")
    database.delete_database_file()
    database.create_database_file()

    # Push the json data into the database.
    print("Pushing JSON data into database...")
    populate_db_from_json(db_service)

    # Update the console
    print("Database processing complete...")
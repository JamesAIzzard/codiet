"""
Module to handle all data sourcing and database population.
"""

import os

from codiet.db import DB_PATH
from codiet.db_population.ingredients import ingredient_datafile_utils
from codiet.db_population.ingredients.ingredient_datafile_utils import apply_to_each_ingredient_datafile as for_all_ingredients
from codiet.db_population import populate_database, reset_database
from codiet.db_population.create_schema import create_schema

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

    # DATABASE CREATION
    reset_database()

    # DATABASE POPULATION
    # Push all of the ingredient .json data into the database
    # print("Pushing datafile data into database...")
    # print("Pushing custom units into database...")
    # populate_database.push_global_custom_units_to_db()
    # print("Pushing global flags into database...")
    # populate_database.push_global_flags_to_db()
    # print("Pushing global nutrients into database...")
    # populate_database.push_global_nutrients_to_db()
    # print("Pushing ingredients into database...")
    # populate_database.push_ingredients_to_db()
    # print("Pushing global recipe tags into database...")
    # populate_database.push_global_recipe_tags_to_db()
    # print("Pushing recipes into database...")
    # populate_database.push_recipes_to_db()

    # Update the console
    print("Database processing complete.")
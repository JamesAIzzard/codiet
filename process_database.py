import os
import json

from codiet.db import DB_PATH
from codiet.db_construction import FLAG_DATA_FILE, NUTRIENT_DATA_FILE
from codiet.db.database_service import DatabaseService
from codiet.db_construction import populate_database
from codiet.db_construction.create_schema import create_schema

if __name__ == '__main__':
    # First, remove any database that exists
    if os.path.exists(DB_PATH):
        print(f"Removing existing database at {DB_PATH}")
        os.remove(DB_PATH)

    # Rebuild the database schema
    create_schema()

    with DatabaseService() as db_service:
        # Grab the flags from the datafile
        global_flags = json.load(open(FLAG_DATA_FILE))
        # Push them to the database
        populate_database.push_flags_to_db(global_flags, db_service)

        # Grab the nutrients from the datafile
        nutrient_data = json.load(open(NUTRIENT_DATA_FILE))
        populate_database.push_nutrients_to_db(nutrient_data, db_service)

        # Work through the existing datafiles and remove any redundant flags and nutrients
        populate_database.remove_redundant_flags_from_datafiles(global_flags)
        populate_database.remove_redundant_nutrients_from_datafiles(db_service)

        # Initialise the ingredient datafiles from the wishlist and template
        populate_database.init_ingredient_datafiles(db_service)

        # Use the OpenAI model to populate the ingredient datafiles
        populate_database.populate_ingredient_datafiles(db_service)

        # Push all of the final data to the database
        populate_database.push_ingredients_to_db(db_service)
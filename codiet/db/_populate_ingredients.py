import os, json

INGREDIENT_DATA_DIR = os.path.join(os.path.dirname(__file__), 'ingredient_data')

def _populate_ingredients(db_service):
    # Work through each .json file in the ingredient_data directory
    for file in os.listdir(INGREDIENT_DATA_DIR):
        # Open the file and load the data
        with open(os.path.join(INGREDIENT_DATA_DIR, file)) as f:
            data = json.load(f)

        # Add the ingredient name to the database

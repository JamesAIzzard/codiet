import os

from codiet.utils.json import read_json_data

TEST_DATA_DIRNAME = "test_recipe_data"
TEST_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), TEST_DATA_DIRNAME)

def fetch_test_recipe_data(recipe_name: str) -> dict:
    try:
        return read_json_data(f"{TEST_DATA_FILEPATH}/{recipe_name}.json")
    except FileNotFoundError:
        raise ValueError(f"Test data for recipe '{recipe_name}' not found.")
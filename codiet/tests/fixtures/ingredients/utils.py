import os

from codiet.utils.json import read_json_data

TEST_DATA_DIRNAME = "test_ingredient_data"
TEST_DATA_FILEPATH = os.path.join(os.path.dirname(__file__), TEST_DATA_DIRNAME)

def fetch_test_ingredient_data(ingredient_name: str) -> dict:
    try:
        return read_json_data(f"{TEST_DATA_FILEPATH}/{ingredient_name}.json")
    except FileNotFoundError:
        raise ValueError(f"Test data for ingredient '{ingredient_name}' not found.")
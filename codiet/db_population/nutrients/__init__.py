import json
import os
from typing import Dict, Any

from codiet.db.repository import Repository

GLOBAL_NUTRIENTS_FILENAME = 'global_nutrients.json'
GLOBAL_NUTRIENTS_FILEPATH = os.path.join(os.path.dirname(__file__), GLOBAL_NUTRIENTS_FILENAME)

def get_global_nutrients() -> Dict[str, Any]:
    """Returns the global nutrients data from the JSON file."""
    with open(GLOBAL_NUTRIENTS_FILEPATH, 'r') as file:
        return json.load(file)

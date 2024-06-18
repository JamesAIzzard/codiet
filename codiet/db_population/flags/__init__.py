import json
import os

GLOBAL_FLAGS_FILENAME = 'global_flags.json'
GLOBAL_FLAGS_FILEPATH = os.path.join(os.path.dirname(__file__), GLOBAL_FLAGS_FILENAME)

def get_global_flags() -> list[str]:
    """Returns a list of global flag names as strings."""
    with open(GLOBAL_FLAGS_FILEPATH, 'r') as file:
        return json.load(file)

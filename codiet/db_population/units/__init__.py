import os
import json

_cached_global_units: dict|None = None

GLOBAL_CUSTOM_UNITS_FILENAME = "global_custom_units.json"

def get_global_custom_units() -> dict:
    """Get the global custom units from the .json file."""
    global _cached_global_units
    if _cached_global_units is None:
        with open(os.path.join(os.path.dirname(__file__), GLOBAL_CUSTOM_UNITS_FILENAME)) as file:
            _cached_global_units = json.load(file)
    return _cached_global_units # type: ignore
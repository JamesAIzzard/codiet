import os
import json
from typing import Any

from codiet.models.units.unit import Unit

_cached_global_units: dict[str, Unit] | None = None

GLOBAL_UNITS_FILENAME = "global_units.json"

def read_global_units_from_json() -> dict[str, Unit]:
    """Reads the units JSON datafile and returns the data as a dictionary
    of units.
    Notes:
        This is currently very unlikely to change during runtime, so we cache
        the result to avoid reading the file multiple times.
    """
    global _cached_global_units
    # If the global units have not been read yet
    if _cached_global_units is None:
        # Init the dict
        _cached_global_units = {}
        # Read the JSON file
        with open(os.path.join(os.path.dirname(__file__), GLOBAL_UNITS_FILENAME)) as file:
            # Load the data
            data = json.load(file)
            # Iterate over the data
            for unit_name, unit_data in data.items():
                # Create a new unit object
                unit = Unit(
                    unit_name=unit_name,
                    single_display_name=unit_data["single_display_name"],
                    plural_display_name=unit_data["plural_display_name"],
                    type=unit_data["type"],
                    aliases=unit_data.get("aliases", None)
                )
                # Add the unit to the dict
                _cached_global_units[unit_name] = unit
    return _cached_global_units # type: ignore

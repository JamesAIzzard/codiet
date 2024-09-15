"""This file contains functions for reading unit data from JSON files."""

import json
from typing import Any, Collection

from codiet.utils import IUC
from codiet.model.units import Unit, UnitConversion
from .configs import UNITS_FILEPATH, UNIT_CONVERSIONS_FILEPATH

def read_units_from_json(units_json_filepath: str=UNITS_FILEPATH) -> IUC[Unit]:
    """Reads the units JSON datafile and returns the data as a set of units."""

    units = []

    data = _read_dict_from_json(units_json_filepath)

    for unit_name, unit_data in data.items():
        unit = Unit(
            unit_name=unit_name,
            single_display_name=unit_data['single_display_name'],
            plural_display_name=unit_data['plural_display_name'],
            type=unit_data['type'],
            aliases=set(unit_data.get('aliases', []))
        )
        units.append(unit)

    return IUC(units)

def read_global_unit_conversions_from_json(
        global_units: Collection[Unit],
        unit_conversions_json_filepath: str=UNIT_CONVERSIONS_FILEPATH
    ) -> IUC[UnitConversion]:
    """Creates unit conversion instances from JSON data using provided unit collection."""

    conversions = []
    data = _read_dict_from_json(unit_conversions_json_filepath)

    # For efficiency, create a dictionary for quick unit lookup
    unit_dict = {unit.unit_name: unit for unit in global_units}

    for conversion_key, conversion_data in data.items():
        from_unit = unit_dict.get(conversion_data['from_unit'])
        to_unit = unit_dict.get(conversion_data['to_unit'])
        
        if from_unit is None or to_unit is None:
            print(f"Warning: Could not find units for conversion {conversion_key}. Skipping.")
            continue

        conversion = UnitConversion(
            from_unit=from_unit,
            to_unit=to_unit,
            from_unit_qty=conversion_data['from_quantity'],
            to_unit_qty=conversion_data['to_quantity']
        )
        
        conversions.append(conversion)

    return IUC(conversions)

def _read_dict_from_json(json_filepath: str) -> dict[str, Any]:
    """Reads a dictionary from a JSON file."""
    with open(json_filepath, 'r') as f:
        return json.load(f)
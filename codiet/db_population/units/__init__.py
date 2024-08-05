import os
import json
from typing import Dict, Any

from codiet.utils.map import Map
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion

GLOBAL_UNITS_FILENAME = "global_units.json"
GLOBAL_UNITS_FILEPATH = os.path.join(os.path.dirname(__file__), GLOBAL_UNITS_FILENAME)

_cached_global_units: set[Unit] | None = None
_cached_global_unit_conversions: set[UnitConversion] | None = None

def read_global_units_from_json(global_units_filepath: str=GLOBAL_UNITS_FILEPATH) -> set[Unit]:
    """Reads the units JSON datafile and returns the data as a set of units."""
    global _cached_global_units
    
    if _cached_global_units is not None:
        return _cached_global_units

    units = set()
    with open(global_units_filepath, 'r') as f:
        data: Dict[str, Dict[str, Any]] = json.load(f)

    for unit_name, unit_data in data.items():
        unit = Unit(
            unit_name=unit_name,
            single_display_name=unit_data['single_display_name'],
            plural_display_name=unit_data['plural_display_name'],
            type=unit_data['type'],
            aliases=set(unit_data.get('aliases', []))
        )
        units.add(unit)

    _cached_global_units = units
    return units

def read_global_unit_conversions_from_json(global_units_filepath: str=GLOBAL_UNITS_FILEPATH) -> set[UnitConversion]:
    """Reads the unit conversions JSON datafile and returns the data as a set of unit conversions."""
    global _cached_global_unit_conversions
    
    if _cached_global_unit_conversions is not None:
        return _cached_global_unit_conversions

    units = read_global_units_from_json(global_units_filepath)
    unit_dict = {unit.unit_name: unit for unit in units}

    conversions = set()
    with open(global_units_filepath, 'r') as f:
        data: Dict[str, Dict[str, Any]] = json.load(f)

    for from_unit_name, unit_data in data.items():
        from_unit = unit_dict[from_unit_name]
        for to_unit_name, conversion_factor in unit_data.get('conversions', {}).items():
            to_unit = unit_dict[to_unit_name]
            conversion = UnitConversion(
                from_unit=from_unit,
                to_unit=to_unit,
                from_unit_qty=1,
                to_unit_qty=conversion_factor
            )
            conversions.add(conversion)

    _cached_global_unit_conversions = conversions
    return conversions

def global_name_unit_map() -> Map[str, Unit]:
    """Returns a map of unit names to units."""
    units = read_global_units_from_json()
    
    # Init and populate the map
    name_unit_map = Map[str, Unit]()
    for unit in units:
        name_unit_map.add_mapping(unit.unit_name, unit)

    return name_unit_map
        
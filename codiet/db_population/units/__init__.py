import os
import json
from typing import Dict, Any

from codiet.utils.map import Map
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion

UNITS_FILENAME = "global_units.json"
UNITS_FILEPATH = os.path.join(os.path.dirname(__file__), UNITS_FILENAME)

_cached_units: set[Unit] | None = None
_cached_global_unit_conversions: set[UnitConversion] | None = None

def read_units_from_json(global_units_filepath: str=UNITS_FILEPATH) -> set[Unit]:
    """Reads the units JSON datafile and returns the data as a set of units."""
    global _cached_units

    if _cached_global_unit_conversions is None:
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

        _cached_units = units

    return _cached_units # type: ignore # cached at this point

def read_global_unit_conversions_from_json(global_units_filepath: str=UNITS_FILEPATH) -> set[UnitConversion]:
    """Reads the unit conversions JSON datafile and returns the data as a set of unit conversions."""
    global _cached_global_unit_conversions
    
    if _cached_global_unit_conversions is None:
        units = read_units_from_json(global_units_filepath)
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
    
    return _cached_global_unit_conversions # type: ignore # cached at this point

def name_unit_map() -> Map[str, Unit]:
    """Returns a map of unit names to units."""
    units = read_units_from_json()
    
    # Init and populate the map
    name_unit_map = Map[str, Unit]()
    for unit in units:
        name_unit_map.add_mapping(unit.unit_name, unit)

    return name_unit_map
        
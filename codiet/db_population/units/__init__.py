import os
import json
from typing import Any

_cached_global_units: dict|None = None

GLOBAL_UNITS_FILENAME = "global_units.json"

def get_global_units() -> dict[str, Any]:
    """Get the global custom units from the .json file.
    Conversion factor is the amount you need to multiply this unit by
    to get the other unit. For example, if you have 1 kg, you can convert
    it to 1000 g by multiplying by 1000. So the conversion factor is 1000.
    Returns:
        "unit_name": {
            "type": "mass/volume/grouping",
            "single_display_name": "...",
            "plural_display_name": "...",
            "aliases": ["...", "..."],
            "conversions": {
                other_unit_name: conversion_factor,
            }
        },
    """
    global _cached_global_units
    if _cached_global_units is None:
        with open(os.path.join(os.path.dirname(__file__), GLOBAL_UNITS_FILENAME)) as file:
            _cached_global_units = json.load(file)
    return _cached_global_units # type: ignore
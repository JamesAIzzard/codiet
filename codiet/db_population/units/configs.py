"""Configurations for populating the units data in the database."""

import os

_base_filepath = os.path.dirname(__file__)
UNITS_FILENAME = "global_units.json"
UNIT_CONVERSIONS_FILENAME = "global_unit_conversions.json"
UNITS_FILEPATH = os.path.join(_base_filepath, UNITS_FILENAME)
UNIT_CONVERSIONS_FILEPATH = os.path.join(_base_filepath, UNIT_CONVERSIONS_FILENAME)
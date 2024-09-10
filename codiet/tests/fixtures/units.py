"""Test fixtures for the units module."""

from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import GlobalUnitConversion

def get_test_units() -> dict[str, Unit]:
    """Instantiates a dictionary of units for testing purposes."""
    return {
        "gram": Unit(
            unit_name="gram",
            single_display_name="g",
            plural_display_name="g",
            type="mass"
        ),
        "kilogram": Unit(
            unit_name="kilogram",
            single_display_name="kg",
            plural_display_name="kg",
            aliases=["kgs"],
            type="mass"),
        "millilitre": Unit(
            unit_name="millilitre",
            single_display_name="ml",
            plural_display_name="ml",
            type="volume"
        ),
        "litre": Unit(
            unit_name="litre",
            single_display_name="l",
            plural_display_name="l",
            type="volume"
        ),
        "slice": Unit(
            unit_name="slice",
            single_display_name="slice",
            plural_display_name="slices",
            type="grouping"
        )
    }

def get_test_global_unit_conversions(test_units:dict[str, Unit]|None=None) -> dict[str, GlobalUnitConversion]:
    """Instantiates a dictionary of global unit conversions for testing purposes."""
    # Init the test units if not supplied
    if test_units is None:
        test_units = get_test_units()
    
    return {
        "millilitre-litre": GlobalUnitConversion(
            from_unit=test_units["millilitre"],
            to_unit=test_units["litre"],
            from_unit_qty=1000,
            to_unit_qty=1
        ),
        "gram-kilogram": GlobalUnitConversion(
            from_unit=test_units["gram"],
            to_unit=test_units["kilogram"],
            from_unit_qty=1000,
            to_unit_qty=1
        ),
    }
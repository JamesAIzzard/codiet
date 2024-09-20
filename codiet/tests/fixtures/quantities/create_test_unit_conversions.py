from typing import TYPE_CHECKING

from codiet.model.quantities import UnitConversion, Quantity

if TYPE_CHECKING:
    from codiet.model.quantities import Unit

def create_test_global_unit_conversions(units:dict[str, 'Unit']) -> dict[tuple[str, str], UnitConversion]:
    return {
        ("millilitre", "litre"): UnitConversion(
            (
                Quantity(unit=units["millilitre"], value=1000),
                Quantity(unit=units["litre"], value=1),
            )
        ),
        ("gram", "kilogram"): UnitConversion(
            (
                Quantity(unit=units["gram"], value=1000),
                Quantity(unit=units["kilogram"], value=1),
            )
        )
    }

def create_test_entity_unit_conversions(units:dict[str, 'Unit']) -> dict[tuple[str, str], UnitConversion]:
    return {
        ("gram", "millilitre"): UnitConversion(
            (
                Quantity(unit=units["gram"], value=1),
                Quantity(unit=units["millilitre"], value=1),
            )
        ),
        ("gram", "slice"): UnitConversion(
            (
                Quantity(unit=units["gram"], value=100),
                Quantity(unit=units["whole"], value=1),
            )
        )
    }
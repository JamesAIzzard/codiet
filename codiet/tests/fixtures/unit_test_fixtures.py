"""Test fixtures for the units module."""
from typing import TYPE_CHECKING

from codiet.model.units import Unit, UnitConversion

if TYPE_CHECKING:
    from codiet.db.database_service import DatabaseService

class UnitTestFixtures:
    """Test fixtures for the units module."""

    def __init__(self) -> None:
        self._units:dict[str, Unit]|None = None
        self._database_units_setup:bool = False
        self._global_unit_conversions:dict[tuple[str, str], UnitConversion]|None = None
        self._database_global_unit_conversions_setup:bool = False

    @property
    def units(self) -> dict[str, Unit]:
        """Returns the test units."""
        if self._units is None:
            self._units = self._create_test_units()
        return self._units
    
    @property
    def gram(self) -> Unit:
        """Returns the gram unit."""
        return self.units["gram"]

    @property
    def global_unit_conversions(self) -> dict[tuple[str, str], UnitConversion]:
        """Returns the test global unit conversions.
        The dictionary key is a tuple of the from and to unit names.
        """
        if self._global_unit_conversions is None:
            self._global_unit_conversions = self._create_test_global_unit_conversions()
        return self._global_unit_conversions

    def get_unit_by_name(self, unit_name:str) -> Unit:
        """Returns a unit by name."""
        return self.units[unit_name]

    def get_global_unit_conversion_by_name(self, conversion_name:tuple[str, str]) -> UnitConversion:
        """Returns a global unit conversion by name."""
        return self.global_unit_conversions[conversion_name]

    def setup_database_units(self, db_service:'DatabaseService') -> None:
        """Sets up the test units in the database."""
        db_service.units.create_units(self.units.values())
        self._database_units_setup = True

    def setup_database_global_unit_conversions(self, db_service:'DatabaseService') -> None:
        """Sets up the test global unit conversions in the database."""
        if not self._database_units_setup:
            self.setup_database_units(db_service=db_service)
        db_service.units.create_global_unit_conversions(self.global_unit_conversions.values())
        self._database_global_unit_conversions_setup = True

    def _create_test_units(self) -> dict[str, Unit]:
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

    def _create_test_global_unit_conversions(self) -> dict[tuple[str, str], UnitConversion]:
        """Instantiates a dictionary of global unit conversions for testing purposes."""
        return {
            ("millilitre", "litre"): UnitConversion(
                from_unit=self.units["millilitre"],
                to_unit=self.units["litre"],
                from_unit_qty=1000,
                to_unit_qty=1
            ),
            ("gram", "kilogram"): UnitConversion(
                from_unit=self.units["gram"],
                to_unit=self.units["kilogram"],
                from_unit_qty=1000,
                to_unit_qty=1
            ),
        }
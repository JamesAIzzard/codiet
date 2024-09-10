"""Test fixtures for the units module."""

from codiet.db.database_service import DatabaseService
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import GlobalUnitConversion

class UnitsTestFixtures:
    """Test fixtures for the units module.
    Accepts a DatabaseService instance to interact with the database, and
    provides various methods to create test units and unit conversions.
    """

    def __init__(self, db_service:DatabaseService) -> None:
        self._db_service = db_service
        self._test_units:dict[str, Unit]|None = None
        self._test_units_setup:bool = False
        self._test_global_unit_conversions:dict[str, GlobalUnitConversion]|None = None
        self._test_global_unit_conversions_setup:bool = False

    @property
    def test_units(self) -> dict[str, Unit]:
        """Returns the test units."""
        if self._test_units is None:
            self._test_units = self._create_test_units()
        return self._test_units
    
    @property
    def test_global_unit_conversions(self) -> dict[str, GlobalUnitConversion]:
        """Returns the test global unit conversions."""
        if self._test_global_unit_conversions is None:
            self._test_global_unit_conversions = self._create_test_global_unit_conversions()
        return self._test_global_unit_conversions

    def setup_test_units(self) -> None:
        """Sets up the test units in the database."""
        self._db_service.units.create_units(self.test_units.values())
        self._test_units_setup = True

    def setup_test_global_unit_conversions(self) -> None:
        """Sets up the test global unit conversions in the database."""
        if not self._test_units_setup:
            self.setup_test_units()
        self._db_service.units.create_global_unit_conversions(self.test_global_unit_conversions.values())
        self._test_global_unit_conversions_setup = True

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

    def _create_test_global_unit_conversions(self) -> dict[str, GlobalUnitConversion]:
        """Instantiates a dictionary of global unit conversions for testing purposes."""
        return {
            "millilitre-litre": GlobalUnitConversion(
                from_unit=self.test_units["millilitre"],
                to_unit=self.test_units["litre"],
                from_unit_qty=1000,
                to_unit_qty=1
            ),
            "gram-kilogram": GlobalUnitConversion(
                from_unit=self.test_units["gram"],
                to_unit=self.test_units["kilogram"],
                from_unit_qty=1000,
                to_unit_qty=1
            ),
        }
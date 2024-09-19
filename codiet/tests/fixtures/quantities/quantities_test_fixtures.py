from typing import TYPE_CHECKING

from codiet.tests.fixtures import BaseTestFixtures
from codiet.model.quantities import Unit, UnitConversion, Quantity

if TYPE_CHECKING:
    from codiet.db.database_service import DatabaseService


class QuantitiesTestFixtures(BaseTestFixtures):
    """Test fixtures for the units module."""

    def __init__(self) -> None:
        self._units: dict[str, Unit] | None = None
        self._database_units_setup: bool = False

        self._global_unit_conversions: dict[tuple[str, str], UnitConversion] | None = (
            None
        )
        self._database_global_unit_conversions_setup: bool = False

        self._entity_unit_conversions: dict[tuple[str, str], UnitConversion] | None = None

    @property
    def units(self) -> dict[str, Unit]:
        if self._units is None:
            self._units = self._create_test_units()
        return self._units

    @property
    def gram(self) -> Unit:
        return self.units["gram"]

    @property
    def global_unit_conversions(self) -> dict[tuple[str, str], UnitConversion]:
        """Returns the test global unit conversions.
        The dictionary key is a tuple of the from and to unit names.
        """
        if self._global_unit_conversions is None:
            self._global_unit_conversions = self._create_test_global_unit_conversions()
        return self._global_unit_conversions
    
    @property
    def entity_unit_conversions(self) -> dict[tuple[str, str], UnitConversion]:
        """Returns the test entity unit conversions.
        The dictionary key is a tuple of the from and to unit names.
        """
        if self._entity_unit_conversions is None:
            self._entity_unit_conversions = self._create_test_entity_unit_conversions()
        return self._entity_unit_conversions

    def get_unit(self, unit_name: str) -> Unit:
        return self.units[unit_name]

    def get_unit_conversion_by_unit_names(
        self, conversion_name: tuple[str, str]
    ) -> UnitConversion:
        all_conversions = {**self.global_unit_conversions, **self.entity_unit_conversions}
        for key, conversion in all_conversions.items():
            if key == conversion_name:
                return conversion
        raise ValueError(f"Unit conversion not found for {conversion_name}")

    def setup_database_units(self, db_service: "DatabaseService") -> None:
        db_service.units.create_units(self.units.values())
        self._database_units_setup = True

    def setup_database_global_unit_conversions(
        self, db_service: "DatabaseService"
    ) -> None:
        if not self._database_units_setup:
            self.setup_database_units(db_service=db_service)
        db_service.units.create_global_unit_conversions(
            self.global_unit_conversions.values()
        )
        self._database_global_unit_conversions_setup = True

    def _create_test_units(self) -> dict[str, Unit]:
        return {
            "gram": Unit(
                name="gram",
                singular_abbreviation="g",
                plural_abbreviation="g",
                type="mass",
            ),
            "kilogram": Unit(
                name="kilogram",
                singular_abbreviation="kg",
                plural_abbreviation="kg",
                aliases=["kgs"],
                type="mass",
            ),
            "millilitre": Unit(
                name="millilitre",
                singular_abbreviation="ml",
                plural_abbreviation="ml",
                type="volume",
            ),
            "litre": Unit(
                name="litre",
                singular_abbreviation="l",
                plural_abbreviation="l",
                type="volume",
            ),
            "slice": Unit(
                name="slice",
                singular_abbreviation="slice",
                plural_abbreviation="slices",
                type="grouping",
            ),
        }

    def _create_test_global_unit_conversions(
        self,
    ) -> dict[tuple[str, str], UnitConversion]:
        return {
            ("millilitre", "litre"): UnitConversion(
                (
                    Quantity(unit=self.units["millilitre"], value=1000),
                    Quantity(unit=self.units["litre"], value=1),
                )
            ),
            ("gram", "kilogram"): UnitConversion(
                (
                    Quantity(unit=self.units["gram"], value=1000),
                    Quantity(unit=self.units["kilogram"], value=1),
                )
            )
        }
    
    def _create_test_entity_unit_conversions(
        self,
    ) -> dict[tuple[str, str], UnitConversion]:
        return {
            ("gram", "millilitre"): UnitConversion(
                (
                    Quantity(unit=self.units["gram"], value=1),
                    Quantity(unit=self.units["millilitre"], value=1),
                )
            ),
            ("gram", "slice"): UnitConversion(
                (
                    Quantity(unit=self.units["gram"], value=100),
                    Quantity(unit=self.units["slice"], value=1),
                )
            )
        }

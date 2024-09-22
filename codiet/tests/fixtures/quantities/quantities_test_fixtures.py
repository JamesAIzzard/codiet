from typing import TYPE_CHECKING

from codiet.tests.fixtures import BaseTestFixture
from .create_test_units import create_test_units
from .create_test_unit_conversions import (
    create_test_global_unit_conversions,
    create_test_entity_unit_conversions,
)
from codiet.model.quantities import Unit, UnitConversion

if TYPE_CHECKING:
    from codiet.db.database_service import DatabaseService


class QuantitiesTestFixtures(BaseTestFixture):

    def __init__(self) -> None:
        super().__init__()
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
            self._units = create_test_units()
        return self._units

    @property
    def gram(self) -> Unit:
        return self.units["gram"]

    @property
    def global_unit_conversions(self) -> dict[tuple[str, str], UnitConversion]:
        if self._global_unit_conversions is None:
            self._global_unit_conversions = create_test_global_unit_conversions(self.units)
        return self._global_unit_conversions
    
    @property
    def entity_unit_conversions(self) -> dict[tuple[str, str], UnitConversion]:
        if self._entity_unit_conversions is None:
            self._entity_unit_conversions = create_test_entity_unit_conversions(self.units)
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

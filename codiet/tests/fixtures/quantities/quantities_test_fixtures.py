import os
from typing import TYPE_CHECKING

from codiet.utils.unique_dict import UniqueDict
from codiet.tests.fixtures import BaseTestFixture
from codiet.db_population.quantities import (
    UnitJSONFetcher,
    UnitConversionJSONFetcher,
    JSONToUnitFactory,
    JSONToUnitConversionFactory,
)

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion

_current_dir = os.path.dirname(__file__)
TEST_UNITS_DATA_DIR_PATH = os.path.join(_current_dir, "test_quantities_data")
TEST_GLOBAL_UNIT_CONVERSIONS_DATA_DIR_PATH = os.path.join(
    _current_dir, "test_quantities_data"
)


class QuantitiesTestFixtures(BaseTestFixture):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._unit_json_fetcher = UnitJSONFetcher(TEST_UNITS_DATA_DIR_PATH)
        self._global_unit_conversion_json_fetcher = UnitConversionJSONFetcher(
            TEST_GLOBAL_UNIT_CONVERSIONS_DATA_DIR_PATH
        )

        self._unit_factory = JSONToUnitFactory()
        self._global_unit_conversion_factory = JSONToUnitConversionFactory(
            get_unit=self.get_unit
        )

        self._units = UniqueDict[str, "Unit"]()
        self._global_unit_conversions = UniqueDict[frozenset[str], "UnitConversion"]()

    def get_unit(self, unit_name: str) -> "Unit":
        try:
            return self._units[unit_name]
        except KeyError:
            unit_data = self._unit_json_fetcher.fetch_data(unit_name)
            unit = self._unit_factory.build(unit_name, unit_data)
            self._units[unit_name] = unit
            return unit

    def get_global_unit_conversion(self, unit_names: frozenset[str]) -> "UnitConversion":
        try:
            return self._global_unit_conversions[unit_names]
        except KeyError:
            conversion_data = self._global_unit_conversion_json_fetcher.fetch_data(
                unit_names
            )
            conversion = self._global_unit_conversion_factory.build(
                unit_names, conversion_data
            )
            self._global_unit_conversions[unit_names] = conversion
            return conversion

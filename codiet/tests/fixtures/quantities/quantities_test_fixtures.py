from typing import TYPE_CHECKING

from codiet.utils.unique_dict import UniqueDict
from codiet.tests.fixtures import BaseTestFixture
from codiet.db_population import get_data_dir_path
from codiet.db_population.quantities import (
    UnitJSONFetcher,
    UnitConversionJSONFetcher,
    JSONToUnitFactory,
    JSONToUnitConversionFactory
)

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion

UNIT_JSON_DIR_PATH = get_data_dir_path("units")
GLOBAL_UNIT_CONVERSIONS_JSON_DIR_PATH = get_data_dir_path("global_unit_conversions")


class QuantitiesTestFixtures(BaseTestFixture):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._unit_json_fetcher = UnitJSONFetcher(UNIT_JSON_DIR_PATH)
        self._global_unit_conversion_json_fetcher = UnitConversionJSONFetcher(
            GLOBAL_UNIT_CONVERSIONS_JSON_DIR_PATH
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

from typing import Any

from ..json_data_fetcher import JSONFetcher

class UnitConversionJSONFetcher(JSONFetcher):

    def fetch_data(self, unit_names:frozenset[str]) -> dict[str, Any]:
        entire_file_data = self._read_entire_file("global_unit_conversions.json")
        indexable_names = list(unit_names)
        conversion_key = '-'.join(indexable_names)
        conversion_key_reversed = '-'.join(indexable_names[::-1])
        try:
            unit_conversion_data = entire_file_data[conversion_key]
        except KeyError:
            unit_conversion_data = entire_file_data[conversion_key_reversed]
        return unit_conversion_data
from typing import Any

from ..json_data_fetcher import JSONFetcher

class UnitJSONFetcher(JSONFetcher):

    def fetch_data(self, unit_name:str) -> dict[str, Any]:
        entire_file_data = self._read_entire_file("units.json")
        return entire_file_data[unit_name]
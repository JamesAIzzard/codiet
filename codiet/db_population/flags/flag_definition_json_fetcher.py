from typing import Any

from ..json_data_fetcher import JSONFetcher

class FlagDefinitionJSONFetcher(JSONFetcher):

    def fetch_data(self, flag_name:str) -> dict[str, Any]:
        entire_file_data = self._read_entire_file("flag_definitions.json")
        return entire_file_data[flag_name]
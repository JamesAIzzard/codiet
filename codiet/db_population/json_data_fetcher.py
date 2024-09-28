from abc import ABC, abstractmethod
from typing import Any
import json
import os

class JSONFetcher(ABC):
    def __init__(self, data_dir_path:str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._data_dir_path = data_dir_path

    @abstractmethod
    def fetch_data(self, key:Any) -> dict[str, Any]:
        raise NotImplementedError
    
    def _read_entire_file(self, filename: str) -> dict[str, Any]:
        file_path = os.path.join(self._data_dir_path, filename)
        with open(file_path, 'r') as file:
            return json.load(file)
        




class IngredientJSONFetcher(JSONFetcher):

    def fetch_data(self, ingredient_name:str) -> dict[str, Any]:
        entire_file_data = self._read_entire_file(f"{ingredient_name.replace(" ", "_")}.json")
        return entire_file_data
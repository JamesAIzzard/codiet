import os
from typing import TYPE_CHECKING, Any

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.data.json_reader import JSONReader

if TYPE_CHECKING:
    from codiet.model.quantities import UnitDTO
    from codiet.model.nutrients import NutrientDTO

class JSONRepository:
    def __init__(self, data_dir: str):
        self._data_dir = data_dir
        self._json_reader = JSONReader()

    def read_unit_data(self, name:str) -> 'UnitDTO':
        entire_file_data = self._json_reader.read_file(os.path.join(self._data_dir, "units.json"))
        unit_data = entire_file_data[name]
        return {
            "name": name,
            "type": unit_data["type"],
            "singular_abbreviation": unit_data["singular_abbreviation"],
            "plural_abbreviation": unit_data["plural_abbreviation"],
            "aliases": unit_data["aliases"]
        }

    def read_all_global_unit_conversion_names(self) -> IUC[str]:
        raise NotImplementedError
    
    def read_nutrient_data(self, name: str) -> 'NutrientDTO':
        all_nutrient_data = self._json_reader.read_file(os.path.join(self._data_dir, "nutrients.json"))
        
        def find_nutrient(data, target_name, parent_name=None) -> 'NutrientDTO':
            for key, value in data.items():
                if key == target_name:
                    return {
                        "name": target_name,
                        "aliases": value["aliases"],
                        "parent_name": parent_name,
                        "child_names": list(value.get("children", {}).keys())
                    }
                if "children" in value:
                    result = find_nutrient(value["children"], target_name, key)
                    if result:
                        return result
            raise ValueError(f"Nutrient '{target_name}' not found in the data.")

        nutrient_dto = find_nutrient(all_nutrient_data, name)
        
        return nutrient_dto
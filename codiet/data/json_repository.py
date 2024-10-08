import os
from typing import TYPE_CHECKING

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.data.json_reader import JSONReader

if TYPE_CHECKING:
    from codiet.model.quantities import UnitDTO, UnitConversionDTO
    from codiet.model.nutrients import NutrientDTO
    from codiet.model.ingredients import IngredientDTO
    from codiet.model.recipes import RecipeDTO


class JSONRepository:
    def __init__(self, data_dir: str):
        self._data_dir = data_dir
        self._json_reader = JSONReader()

    def read_all_unit_names(self) -> IUC[str]:
        entire_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "units.json")
        )
        return IUC(entire_file_data.keys())

    def read_unit_dto(self, name: str) -> "UnitDTO":
        entire_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "units.json")
        )
        unit_data = entire_file_data[name]
        return {
            "name": name,
            "type": unit_data["type"],
            "singular_abbreviation": unit_data["singular_abbreviation"],
            "plural_abbreviation": unit_data["plural_abbreviation"],
            "aliases": unit_data["aliases"],
        }

    def read_all_global_unit_conversion_names(self) -> IUC[tuple[str, str]]:
        entire_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "global_unit_conversions.json")
        )

        conversion_names:list[tuple[str, str]] = []

        for conversion_name in entire_file_data.keys():
            names = conversion_name.split("-")
            conversion_names.append((names[0], names[1]))
        
        return IUC(conversion_names)

    def read_global_unit_conversion_dto(self, names: tuple[str, str]) -> "UnitConversionDTO":
        entire_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "global_unit_conversions.json")
        )
        conversion_name = f"{names[0]}-{names[1]}"
        conversion_data = entire_file_data[conversion_name]
        return {
            "from_quantity": {
                "unit_name": conversion_data["from_quantity"]["unit_name"],
                "value": conversion_data["from_quantity"]["value"],
            },
            "to_quantity": {
                "unit_name": conversion_data["to_quantity"]["unit_name"],
                "value": conversion_data["to_quantity"]["value"],
            },
        }

    def read_nutrient_dto(self, name: str) -> "NutrientDTO":
        all_nutrient_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "nutrients.json")
        )

        def find_nutrient(data, target_name, parent_name=None) -> "NutrientDTO|None":
            if target_name in data:
                return {
                    "name": target_name,
                    "aliases": data[target_name].get("aliases", []),
                    "parent_name": parent_name,
                    "child_names": list(data[target_name].get("children", {}).keys()),
                }
            
            for key, value in data.items():
                if "children" in value:
                    result = find_nutrient(value["children"], target_name, key)
                    if result:
                        return result
            
            return None

        nutrient_dto = find_nutrient(all_nutrient_data, name)
        
        if nutrient_dto is None:
            raise ValueError(f"Nutrient '{name}' not found in the data.")

        return nutrient_dto

    def read_ingredient_dto(self, name: str) -> "IngredientDTO":
        ingredient_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "ingredients", name + ".json")
        )

        unit_conversions = []
        for unit_conversion_data in ingredient_file_data["unit_conversions"]:
            unit_conversions.append(
                {
                    "from_quantity": {
                        "unit_name": unit_conversion_data[0][0],
                        "value": unit_conversion_data[0][1],
                    },
                    "to_quantity": {
                        "unit_name": unit_conversion_data[1][0],
                        "value": unit_conversion_data[1][1],
                    },
                }
            )

        quantity_cost = {
            "cost": ingredient_file_data["quantity_cost"]["cost"],
            "quantity": {
                "unit_name": ingredient_file_data["quantity_cost"]["quantity"][0],
                "value": ingredient_file_data["quantity_cost"]["quantity"][1],
            }
        }

        flags = {}
        for flag_name, flag_value in ingredient_file_data["flags"].items():
            flags[flag_name] = {
                "name": flag_name,
                "value": flag_value,
            }

        nutrient_quantities = {}
        for nutrient_name, nutrient_qty_data in ingredient_file_data["nutrient_quantities_per_gram"].items():
            nutrient_quantities[nutrient_name] = {
                "nutrient_name": nutrient_name,
                "quantity": {
                    "unit_name": nutrient_qty_data[0],
                    "value": nutrient_qty_data[1],
                },
            }

        return {
            "name": name,
            "description": ingredient_file_data["description"],
            "unit_conversions": unit_conversions,
            "standard_unit": ingredient_file_data["standard_unit"],
            "quantity_cost": quantity_cost,
            "gi": ingredient_file_data["gi"],
            "flags": flags,
            "nutrient_quantities_per_gram": nutrient_quantities,
        }

    def read_recipe_dto(self, recipe_name: str) -> "RecipeDTO":
        recipe_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "recipes", recipe_name + ".json")
        )

        ingredient_quantities = {}
        for ingredient_name, quantity_data in recipe_file_data[
            "ingredient_quantities"
        ].items():
            ingredient_quantities[ingredient_name] = {
                "ingredient_name": ingredient_name,
                "quantity": {
                    "unit_name": quantity_data["unit"],
                    "value": quantity_data["value"],
                },
            }

        serve_time_windows = []
        for time_window in recipe_file_data["serve_time_windows"]:
            start_time, end_time = time_window.split("-")
            serve_time_windows.append(
                {
                    "start_hh_mm": start_time,
                    "end_hh_mm": end_time,
                }
            )

        tags = []
        for tag_name in recipe_file_data["tags"]:
            tags.append(
                {
                    "name": tag_name,
                }
            )

        recipe_data = {
            "name": recipe_name,
            "use_as_ingredient": recipe_file_data["use_as_ingredient"],
            "description": recipe_file_data["description"],
            "instructions": recipe_file_data["instructions"],
            "ingredient_quantities": ingredient_quantities,
            "serve_time_windows": serve_time_windows,
            "tags": tags,
        }

        return recipe_data

import os
from typing import TYPE_CHECKING

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.data.json_reader import JSONReader

if TYPE_CHECKING:
    from codiet.model.quantities import UnitDTO, UnitConversionDTO
    from codiet.model.nutrients import NutrientDTO
    from codiet.model.cost import QuantityCostDTO
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

    def read_all_global_unit_conversion_names(self) -> IUC[frozenset[str]]:
        entire_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "global_unit_conversions.json")
        )

        conversion_names: list[frozenset[str]] = []

        for conversion_name in entire_file_data.keys():
            names = conversion_name.split("-")
            conversion_names.append(frozenset((names[0], names[1])))

        return IUC(conversion_names)

    def read_global_unit_conversion_dto(
        self, names: frozenset[str]
    ) -> "UnitConversionDTO":
        entire_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "global_unit_conversions.json")
        )
        names_forward = "-".join(tuple(names))
        names_backward = "-".join(tuple(names)[::-1])
        if names_forward in entire_file_data:
            conversion_name = names_forward
        elif names_backward in entire_file_data:
            conversion_name = names_backward
        else:
            raise ValueError(f"Unit conversion '{names}' not found in the data.")
        conversion_data = entire_file_data[conversion_name]
        return conversion_data

    def read_all_nutrient_names(self) -> IUC[str]:
        all_nutrient_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "nutrients.json")
        )

        def find_all_nutrients(data) -> list[str]:
            nutrient_names = []
            for key, value in data.items():
                if "cals_per_gram" in value.keys():
                    nutrient_names.append(key)
                if "children" in value:
                    nutrient_names.extend(find_all_nutrients(value["children"]))
            return nutrient_names

        return IUC(find_all_nutrients(all_nutrient_data))

    def read_nutrient_dto(self, name: str) -> "NutrientDTO":
        all_nutrient_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "nutrients.json")
        )

        def find_nutrient(data, target_name, parent_name=None) -> "NutrientDTO|None":

            if target_name not in data:
                for key, value in data.items():
                    if "children" in value:
                        result = find_nutrient(value["children"], target_name, key)
                        if result:
                            return result
            else:
                if "cals_per_gram" in data[target_name].keys():
                    cals_per_gram = data[target_name]["cals_per_gram"]
                else:
                    cals_per_gram = 0

                if target_name in data:
                    return {
                        "name": target_name,
                        "cals_per_gram": cals_per_gram,
                        "aliases": data[target_name].get("aliases", []),
                        "parent_name": parent_name,
                        "child_names": list(
                            data[target_name].get("children", {}).keys()
                        ),
                    }

            return None

        nutrient_dto = find_nutrient(all_nutrient_data, name)

        if nutrient_dto is None:
            raise ValueError(f"Nutrient '{name}' not found in the data.")

        return nutrient_dto

    def read_all_ingredient_names(self) -> IUC[str]:
        ingredient_files = os.listdir(os.path.join(self._data_dir, "ingredients"))
        ingredient_names = [name.split(".")[0] for name in ingredient_files]
        return IUC(ingredient_names)

    def read_ingredient_dto(self, name: str) -> "IngredientDTO":
        ingredient_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "ingredients", name + ".json")
        )

        unit_conversions = {}
        for conversion_data in ingredient_file_data["unit_conversions"]:
            key = frozenset(
                (
                    conversion_data["from_quantity"]["unit_name"],
                    conversion_data["to_quantity"]["unit_name"],
                )
            )
            unit_conversions[key] = conversion_data

        quantity_cost:"QuantityCostDTO" = {
            "cost": ingredient_file_data["quantity_cost"]["cost"],
            "quantity": ingredient_file_data["quantity_cost"]["quantity"],
        }

        flags = {}
        for flag_name, flag_value in ingredient_file_data["flags"].items():
            flags[flag_name] = {
                "name": flag_name,
                "value": flag_value,
            }

        nutrient_quantities = {}
        for nutrient_name, nutrient_qty_data in ingredient_file_data[
            "nutrient_quantities_per_gram"
        ].items():
            nutrient_quantities[nutrient_name] = {
                "nutrient_name": nutrient_name,
                "quantity": nutrient_qty_data,
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

    def read_all_recipe_names(self) -> IUC[str]:
        recipe_files = os.listdir(os.path.join(self._data_dir, "recipes"))
        recipe_names = [name.split(".")[0] for name in recipe_files]
        return IUC(recipe_names)

    def read_recipe_dto(self, name: str) -> "RecipeDTO":
        recipe_file_data = self._json_reader.read_file(
            os.path.join(self._data_dir, "recipes", name + ".json")
        )

        ingredient_quantities = {}
        for ingredient_name, quantity_data in recipe_file_data[
            "ingredient_quantities"
        ].items():
            ingredient_quantities[ingredient_name] = {
                "ingredient_name": ingredient_name,
                "quantity": quantity_data,
            }

        serve_time_windows = []
        for time_window in recipe_file_data["serve_time_windows"]:
            serve_time_windows.append(time_window)

        tags = []
        for tag_name in recipe_file_data["tags"]:
            tags.append(
                {
                    "name": tag_name,
                }
            )

        recipe_data:"RecipeDTO" = {
            "name": name,
            "use_as_ingredient": recipe_file_data["use_as_ingredient"],
            "description": recipe_file_data["description"],
            "instructions": recipe_file_data["instructions"],
            "ingredient_quantities": ingredient_quantities,
            "serve_time_windows": serve_time_windows,
            "tags": tags,
        }

        return recipe_data

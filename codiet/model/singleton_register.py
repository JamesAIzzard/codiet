from typing import TYPE_CHECKING

from codiet.utils.unique_dict import UniqueDict as UD

if TYPE_CHECKING:
    from codiet.data.database_service import DatabaseService
    from codiet.model.quantities import (
        Unit,
        UnitConversion,
        QuantitiesFactory,
    )
    from codiet.model.nutrients import Nutrient
    from codiet.model.flags import FlagDefinition
    from codiet.model.tags import Tag, TagFactory, TagDTO
    from codiet.model.ingredients import Ingredient


class SingletonRegister:
    def __init__(self):
        self._database_service: "DatabaseService"
        self._quantities_factory: "QuantitiesFactory"
        self._tag_factory: "TagFactory"

        self._units = UD[str, "Unit"]()
        self._unit_conversions = UD[frozenset[str], "UnitConversion"]()
        self._nutrients = UD[str, "Nutrient"]()
        self._tags = UD[str, "Tag"]()
        self._flag_definitions = UD[str, "FlagDefinition"]()
        self._ingredients = UD[str, "Ingredient"]()

    def initialise(
        self,
        database_service: "DatabaseService",
        quantities_factory: "QuantitiesFactory",
        tag_factory: "TagFactory",
    ) -> "SingletonRegister":
        self._database_service = database_service
        self._quantities_factory = quantities_factory
        self._tag_factory = tag_factory
        return self

    def get_unit(self, unit_name: str) -> "Unit":
        if unit_name not in self._units:
            self._units[unit_name] = self._database_service.read_unit(unit_name)
        return self._units[unit_name]

    def get_global_unit_conversion(
        self, unit_conversion_key: frozenset[str]
    ) -> "UnitConversion":
        if unit_conversion_key not in self._unit_conversions:
            self._unit_conversions[unit_conversion_key] = (
                self._database_service.read_global_unit_conversion(unit_conversion_key)
            )
        return self._unit_conversions[unit_conversion_key]

    def get_global_unit_conversions(self) -> dict[frozenset[str], "UnitConversion"]:
        conversion_keys = self._database_service.read_all_global_unit_conversion_names()

        conversions = {}
        for key in conversion_keys:
            conversions[key] = self.get_global_unit_conversion(key)

        return conversions

    def get_flag_definition(self, flag_name: str) -> "FlagDefinition":
        if flag_name not in self._flag_definitions:
            self._flag_definitions[flag_name] = self._database_service.read_flag_definition(
                flag_name
            )
        return self._flag_definitions[flag_name]

    def get_all_flag_definitions(self) -> dict[str, "FlagDefinition"]:
        flag_names = self._database_service.read_all_flag_names()

        flag_definitions = {}
        for flag_name in flag_names:
            flag_definitions[flag_name] = self.get_flag_definition(flag_name)

        return flag_definitions

    def get_nutrient(self, nutrient_name: str) -> "Nutrient":
        nutrient_name = nutrient_name.lower()
        try:
            return self._nutrients[nutrient_name]
        except KeyError:
            self._nutrients[nutrient_name] = self._database_service.read_nutrient(
                nutrient_name
            )
            return self._nutrients[nutrient_name]

    def get_tag(self, tag_name: str) -> "Tag":
        try:
            return self._tags[tag_name]
        except KeyError:
            tag_dto:"TagDTO" = {"name": tag_name}
            self._tags[tag_name] = self._tag_factory.create_tag_from_dto(tag_dto)
            return self._tags[tag_name]

    def get_ingredient(self, ingredient_name: str) -> "Ingredient":
        try:
            return self._ingredients[ingredient_name]
        except KeyError:
            self._ingredients[ingredient_name] = self._database_service.read_ingredient(
                ingredient_name
            )
            return self._ingredients[ingredient_name]

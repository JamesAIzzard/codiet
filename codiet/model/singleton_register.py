from typing import TYPE_CHECKING

from codiet.utils.unique_dict import UniqueDict as UD
from codiet.model.tags.tag import TagDTO

if TYPE_CHECKING:
    from codiet.data.database_service import DatabaseService
    from codiet.model.quantities import Unit
    from codiet.model.nutrients import Nutrient
    from codiet.model.tags import Tag, TagFactory
    from codiet.model.ingredients import Ingredient
    from codiet.model.recipes import Recipe


class SingletonRegister:
    def __init__(self):
        self._database_service: "DatabaseService"
        self._tag_factory: "TagFactory"

        self._units = UD[str, "Unit"]()
        self._nutrients = UD[str, "Nutrient"]()
        self._tags = UD[str, "Tag"]()
        self._ingredients = UD[str, "Ingredient"]()
        self._recipes = UD[str, "Recipe"]()

    def set_database_service(
        self, database_service: "DatabaseService"
    ) -> "SingletonRegister":
        self._database_service = database_service
        return self

    def get_unit(self, unit_name: str) -> "Unit":
        try:
            return self._units[unit_name]
        except KeyError:
            self._units[unit_name] = self._database_service.read_unit(unit_name)
            return self._units[unit_name]
        
    def get_nutrient(self, nutrient_name: str) -> "Nutrient":
        try:
            return self._nutrients[nutrient_name]
        except KeyError:
            self._nutrients[nutrient_name] = self._database_service.read_nutrient(nutrient_name)
            return self._nutrients[nutrient_name]

    def get_tag(self, tag_name: str) -> "Tag":
        try:
            return self._tags[tag_name]
        except KeyError:
            tag_dto = TagDTO(name=tag_name)
            self._tags[tag_name] = self._tag_factory.create_tag_from_dto(tag_dto)
            return self._tags[tag_name]

    def get_ingredient(self, ingredient_name: str) -> "Ingredient":
        try:
            return self._ingredients[ingredient_name]
        except KeyError:
            self._ingredients[ingredient_name] = self._database_service.read_ingredient(ingredient_name)
            return self._ingredients[ingredient_name]

    def get_recipe(self, recipe_name: str) -> "Recipe":
        try:
            return self._recipes[recipe_name]
        except KeyError:
            self._recipes[recipe_name] = self._database_service.read_recipe(recipe_name)
            return self._recipes[recipe_name]

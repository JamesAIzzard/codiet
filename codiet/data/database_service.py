from typing import TYPE_CHECKING

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.model.recipes import Recipe

if TYPE_CHECKING:
    from .repository import Repository
    from codiet.model.quantities import Unit, QuantitiesFactory, UnitConversion
    from codiet.model.nutrients import Nutrient, NutrientFactory
    from codiet.model.ingredients import Ingredient, IngredientFactory
    from codiet.model.recipes import RecipeFactory


class DatabaseService:

    def __init__(self) -> None:

        self._repository: "Repository"

        self._quantities_factory: "QuantitiesFactory"
        self._nutrients_factory: "NutrientFactory"
        self._ingredient_factory: "IngredientFactory"
        self._recipe_factory: "RecipeFactory"

    def read_unit_names(self) -> IUC[str]:
        unit_names = self._repository.read_unit_names()
        return IUC(unit_names)

    def read_unit(self, unit_name: str) -> "Unit":
        unit_dto = self._repository.read_unit_dto(unit_name)
        unit = self._quantities_factory.create_unit_from_dto(unit_dto)
        return unit

    def read_all_global_unit_conversion_names(self) -> IUC[tuple[str, str]]:
        unit_conversion_names = self._repository.read_all_global_unit_conversion_names()
        return IUC(unit_conversion_names)

    def read_global_unit_conversion(self, unit_names: tuple[str, str]) -> "UnitConversion":
        unit_conversion_dto = self._repository.read_global_unit_conversion_dto(unit_names)
        unit_conversion = self._quantities_factory.create_unit_conversion_from_dto(unit_conversion_dto)
        return unit_conversion

    def read_all_utrient_names(self) -> IUC[str]:
        nutrient_names = self._repository.read_nutrient_names()
        return IUC(nutrient_names)

    def read_nutrient(self, nutrient_name: str) -> "Nutrient":
        nutrient_dto = self._repository.read_nutrient_dto(nutrient_name)
        nutrient = self._nutrients_factory.create_nutrient_from_dto(nutrient_dto)
        return nutrient

    def read_all_ingredient_names(self) -> IUC[str]:
        ingredient_names = self._repository.read_ingredient_names()
        return IUC(ingredient_names)

    def read_ingredient(self, ingredient_name: str) -> "Ingredient":
        ingredient_dto = self._repository.read_ingredient_dto(ingredient_name)
        ingredient = self._ingredient_factory.create_ingredient_from_dto(ingredient_dto)
        return ingredient

    def read_all_recipe_names(self) -> IUC[str]:
        recipe_names = self._repository.read_recipe_names()
        return IUC(recipe_names)

    def read_recipe(self, recipe_name: str) -> "Recipe":
        recipe_dto = self._repository.read_recipe_dto(recipe_name)
        recipe = self._recipe_factory.create_recipe_from_dto(recipe_dto)
        return recipe

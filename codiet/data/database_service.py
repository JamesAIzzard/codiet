from typing import TYPE_CHECKING

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.utils.unique_dict import FrozenUniqueDict as FUD
from .exceptions import IngredientNotFoundError, RecipeNotFoundError, NutrientNotFoundError
from codiet.model.recipes import Recipe
from codiet.exceptions.quantities import UnitNotFoundError

if TYPE_CHECKING:
    from .repository import Repository
    from codiet.model.quantities import Unit, QuantitiesFactory, UnitConversion
    from codiet.model.nutrients import Nutrient, NutrientFactory
    from codiet.model.flags import FlagDefinition, FlagFactory
    from codiet.model.ingredients import Ingredient, IngredientFactory
    from codiet.model.recipes import RecipeFactory


class DatabaseService:

    def __init__(self) -> None:

        self._repository: "Repository"

        self._quantities_factory: "QuantitiesFactory"
        self._nutrients_factory: "NutrientFactory"
        self._flag_factory: "FlagFactory"
        self._ingredient_factory: "IngredientFactory"
        self._recipe_factory: "RecipeFactory"

    def initialise(
        self,
        repository: "Repository",
        quantities_factory: "QuantitiesFactory",
        nutrients_factory: "NutrientFactory",
        flag_factory: "FlagFactory",
        ingredient_factory: "IngredientFactory",
        recipe_factory: "RecipeFactory",
    ) -> "DatabaseService":
        self._repository = repository
        self._quantities_factory = quantities_factory
        self._nutrients_factory = nutrients_factory
        self._flag_factory = flag_factory
        self._ingredient_factory = ingredient_factory
        self._recipe_factory = recipe_factory
        return self

    def read_unit_names(self) -> IUC[str]:
        unit_names = self._repository.read_all_unit_names()
        return IUC(unit_names)

    def read_unit(self, unit_name: str) -> "Unit":
        try:
            unit_dto = self._repository.read_unit_dto(unit_name)
        except ValueError:
            raise UnitNotFoundError(unit_name)
        unit = self._quantities_factory.create_unit_from_dto(unit_dto)
        return unit

    def read_all_global_unit_conversion_names(self) -> IUC[frozenset[str]]:
        unit_conversion_names = self._repository.read_all_global_unit_conversion_names()
        return IUC(unit_conversion_names)

    def read_global_unit_conversion(
        self, unit_conversion_key: frozenset[str]
    ) -> "UnitConversion":
        unit_conversion_dto = self._repository.read_global_unit_conversion_dto(
            unit_conversion_key
        )
        unit_conversion = self._quantities_factory.create_unit_conversion_from_dto(
            unit_conversion_dto
        )
        return unit_conversion

    def read_all_flag_names(self) -> IUC[str]:
        flag_names = self._repository.read_all_flag_names()
        return IUC(flag_names)

    def read_flag_definition(self, flag_name: str) -> "FlagDefinition":
        flag_definition_dto = self._repository.read_flag_definition_dto(flag_name)
        flag_definition = self._flag_factory.create_flag_definition_from_dto(
            flag_definition_dto
        )
        return flag_definition

    def read_all_nutrient_names(self) -> IUC[str]:
        nutrient_names = self._repository.read_all_nutrient_names()
        return IUC(nutrient_names)

    def read_nutrient(self, nutrient_name: str) -> "Nutrient":
        try:
            nutrient_dto = self._repository.read_nutrient_dto(nutrient_name)
        except ValueError:
            raise NutrientNotFoundError(nutrient_name)
        nutrient = self._nutrients_factory.create_nutrient_from_dto(nutrient_dto)
        return nutrient

    def read_tag(self, tag_name: str) -> "Tag":
        # TODO: Implement - needs to use the tag factory to convert
        # a tag DTO into a tag object.
        raise NotImplementedError

    def read_all_ingredient_names(self) -> IUC[str]:
        ingredient_names = self._repository.read_all_ingredient_names()
        return IUC(ingredient_names)

    def read_ingredient(self, ingredient_name: str) -> "Ingredient":
        try:
            ingredient_dto = self._repository.read_ingredient_dto(ingredient_name)
        except ValueError:
            raise IngredientNotFoundError(ingredient_name)
        ingredient = self._ingredient_factory.create_ingredient_from_dto(ingredient_dto)
        return ingredient

    def read_all_recipe_names(self) -> IUC[str]:
        recipe_names = self._repository.read_all_recipe_names()
        return IUC(recipe_names)

    def read_recipe(self, recipe_name: str) -> "Recipe":
        try:
            recipe_dto = self._repository.read_recipe_dto(recipe_name)
        except ValueError:
            raise RecipeNotFoundError(recipe_name)
        recipe = self._recipe_factory.create_recipe_from_dto(recipe_dto)
        return recipe
    
    def read_all_recipes(self) -> FUD[str, "Recipe"]:
        recipe_names = self.read_all_recipe_names()
        recipes = {}
        for recipe_name in recipe_names:
            recipe = self.read_recipe(recipe_name)
            recipes[recipe_name] = recipe
        return FUD(recipes)

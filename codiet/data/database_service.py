from typing import TYPE_CHECKING

from codiet.model.recipes import Recipe

if TYPE_CHECKING:
    from .repository import Repository
    from codiet.model.quantities import Unit, QuantitiesFactory
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

    def set_repository(self, repository: "Repository") -> "DatabaseService":
        self._repository = repository
        return self

    def set_quantity_factory(self, unit_factory: "QuantitiesFactory") -> "DatabaseService":
        self._quantities_factory = unit_factory
        return self
    
    def set_ingredient_factory(self, ingredient_factory: "IngredientFactory") -> "DatabaseService":
        self._ingredient_factory = ingredient_factory
        return self

    def set_recipe_factory(self, recipe_factory: "RecipeFactory") -> "DatabaseService":
        self._recipe_factory = recipe_factory
        return self

    def read_unit(self, unit_name: str) -> "Unit":
        unit_dto = self._repository.read_unit_dto(unit_name)
        unit = self._quantities_factory.create_unit_from_dto(unit_dto)
        return unit

    def read_nutrient(self, nutrient_name: str) -> "Nutrient":
        nutrient_dto = self._repository.read_nutrient_dto(nutrient_name)
        nutrient = self._nutrients_factory.create_nutrient_from_dto(nutrient_dto)
        return nutrient

    def read_ingredient(self, ingredient_name: str) -> "Ingredient":
        ingredient_dto = self._repository.read_ingredient_dto(ingredient_name)
        ingredient = self._ingredient_factory.create_ingredient_from_dto(ingredient_dto)
        return ingredient

    def read_recipe(self, recipe_name: str) -> "Recipe":
        recipe_dto = self._repository.read_recipe_dto(recipe_name)
        recipe = self._recipe_factory.create_recipe_from_dto(recipe_dto)
        return recipe

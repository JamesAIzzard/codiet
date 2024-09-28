from typing import TYPE_CHECKING, Callable

from codiet.utils.singleton import SingletonMeta
from codiet.utils.unique_dict import UniqueDict

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion
    from codiet.model.flags import FlagDefinition
    from codiet.model.nutrients import Nutrient
    from codiet.model.recipes import Recipe
    from codiet.model.ingredients import Ingredient

class SingletonRegistry(metaclass=SingletonMeta):
    def __init__(self) -> None:        
        self._units = UniqueDict[str, 'Unit']()
        self._global_unit_conversions = UniqueDict[frozenset[str], 'UnitConversion']()
        self._flag_definitions = UniqueDict[str, 'FlagDefinition']()
        self._nutrients = UniqueDict[str, 'Nutrient']()
        self._recipes = UniqueDict[str, 'Recipe']()
        self._ingredients = UniqueDict[str, 'Ingredient']()

        self._unit_loader: Callable[[str], 'Unit']|None = None
        self._global_unit_conversion_loader: Callable[[frozenset[str]], 'UnitConversion']|None = None
        self._flag_loader: Callable[[str], 'FlagDefinition']|None = None
        self._nutrient_loader: Callable[[str], 'Nutrient']|None = None
        self._recipe_loader: Callable[[str], 'Recipe']|None = None
        self._ingredient_loader: Callable[[str], 'Ingredient']|None = None

    def get_unit(self, name: str) -> 'Unit':
        if self._unit_loader is None:
            raise RuntimeError("Unit loader not set.")
        try:
            return self._units[name]
        except KeyError:
            unit = self._unit_loader(name)
            self._units[name] = unit
            return unit

    def get_global_unit_conversion(self, unit_names: frozenset[str]) -> 'UnitConversion':
        if self._global_unit_conversion_loader is None:
            raise RuntimeError("Unit conversion loader not set.")
        try:
            return self._global_unit_conversions[unit_names]
        except KeyError:
            unit_conversion = self._global_unit_conversion_loader(unit_names)
            self._global_unit_conversions[unit_names] = unit_conversion
            return unit_conversion

    def get_flag_definition(self, name: str) -> 'FlagDefinition':
        if self._flag_loader is None:
            raise RuntimeError("Flag loader not set.")
        try:
            return self._flag_definitions[name]
        except KeyError:
            flag_definition = self._flag_loader(name)
            self._flag_definitions[name] = flag_definition
            return flag_definition

    def get_nutrient(self, name: str) -> 'Nutrient':
        if self._nutrient_loader is None:
            raise RuntimeError("Nutrient loader not set.")
        try:
            return self._nutrients[name]
        except KeyError:
            nutrient = self._nutrient_loader(name)
            self._nutrients[name] = nutrient
            return nutrient

    def get_recipe(self, name: str) -> 'Recipe':
        if self._recipe_loader is None:
            raise RuntimeError("Recipe loader not set.")
        try:
            return self._recipes[name]
        except KeyError:
            recipe = self._recipe_loader(name)
            self._recipes[name] = recipe
            return recipe

    def get_ingredient(self, name: str) -> 'Ingredient':
        if self._ingredient_loader is None:
            raise RuntimeError("Ingredient loader not set.")
        try:
            return self._ingredients[name]
        except KeyError:
            ingredient = self._ingredient_loader(name)
            self._ingredients[name] = ingredient
            return ingredient

    def set_unit_loader(self, loader: Callable[[str], 'Unit']) -> None:
        self._unit_loader = loader

    def set_global_unit_conversion_loader(self, loader: Callable[[frozenset[str]], 'UnitConversion']) -> None:
        self._global_unit_conversion_loader = loader

    def set_flag_loader(self, loader: Callable[[str], 'FlagDefinition']) -> None:
        self._flag_loader = loader

    def set_nutrient_loader(self, loader: Callable[[str], 'Nutrient']) -> None:
        self._nutrient_loader = loader

    def set_recipe_loader(self, loader: Callable[[str], 'Recipe']) -> None:
        self._recipe_loader = loader

    def set_ingredient_loader(self, loader: Callable[[str], 'Ingredient']) -> None:
        self._ingredient_loader = loader
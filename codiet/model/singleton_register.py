from typing import TYPE_CHECKING, Callable, Mapping

from codiet.utils.unique_dict import UniqueDict
from codiet.utils.unique_dict import FrozenUniqueDict as FUD
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion
    from codiet.model.flags import FlagDefinition
    from codiet.model.nutrients import Nutrient
    from codiet.model.tags import Tag
    from codiet.model.recipes import Recipe
    from codiet.model.ingredients import Ingredient


class SingletonRegister:
    """The SingletonRegistry is responsible for providing access to the system's singleton entities
    such as units, unit conversions, flags, nutrients, recipes, and ingredients."""

    _get_all_global_unit_conversion_names: Callable[[], IUC[frozenset[str]]]
    _unit_loader: Callable[[str], "Unit"]
    _global_unit_conversion_loader: Callable[[frozenset[str]], "UnitConversion"]
    _flag_loader: Callable[[str], "FlagDefinition"]
    _nutrient_loader: Callable[[str], "Nutrient"]
    _tag_graph_loader: Callable[[], Mapping[str, "Tag"]]
    _recipe_loader: Callable[[str], "Recipe"]
    _ingredient_loader: Callable[[str], "Ingredient"]

    def __init__(self) -> None:
        self._units = UniqueDict[str, "Unit"]()
        self._global_unit_conversions = UniqueDict[frozenset[str], "UnitConversion"]()
        self._flag_definitions = UniqueDict[str, "FlagDefinition"]()
        self._nutrients = UniqueDict[str, "Nutrient"]()
        self._tags = UniqueDict[str, "Tag"]()
        self._recipes = UniqueDict[str, "Recipe"]()
        self._ingredients = UniqueDict[str, "Ingredient"]()

    @classmethod
    def initialise(
        cls,
        get_all_global_unit_conversion_names: Callable[[], IUC[frozenset[str]]],
        unit_loader: Callable[[str], "Unit"],
        global_unit_conversion_loader: Callable[[frozenset[str]], "UnitConversion"],
        flag_definition_loader: Callable[[str], "FlagDefinition"],
        nutrient_loader: Callable[[str], "Nutrient"],
        tag_graph_loader: Callable[[], Mapping[str, "Tag"]],
        recipe_loader: Callable[[str], "Recipe"],
        ingredient_loader: Callable[[str], "Ingredient"],
    ) -> None:
        cls._get_all_global_unit_conversion_names = (
            get_all_global_unit_conversion_names
        )
        cls._unit_loader = unit_loader
        cls._global_unit_conversion_loader = global_unit_conversion_loader
        cls._flag_loader = flag_definition_loader
        cls._nutrient_loader = nutrient_loader
        cls._tag_graph_loader = tag_graph_loader
        cls._recipe_loader = recipe_loader
        cls._ingredient_loader = ingredient_loader

    def get_unit(self, name: str) -> "Unit":
        if name not in self._units:
            self._units[name] = self._unit_loader(name)
        return self._units[name]

    @property
    def global_unit_conversions(self) -> FUD[frozenset[str], "UnitConversion"]:
        unit_conversion_names = self._get_all_global_unit_conversion_names()

        for unit_names in unit_conversion_names:
            if unit_names not in self._global_unit_conversions:
                unit_conversion = self._global_unit_conversion_loader(unit_names)
                self._global_unit_conversions[unit_names] = unit_conversion

        return FUD(self._global_unit_conversions)

    def get_global_unit_conversion(
        self, unit_names: frozenset[str]
    ) -> "UnitConversion":
        if self._global_unit_conversion_loader is None:
            raise RuntimeError("Unit conversion loader not set.")
        try:
            return self._global_unit_conversions[unit_names]
        except KeyError:
            unit_conversion = self._global_unit_conversion_loader(unit_names)
            self._global_unit_conversions[unit_names] = unit_conversion
            return unit_conversion

    def get_flag_definition(self, name: str) -> "FlagDefinition":
        if self._flag_loader is None:
            raise RuntimeError("Flag loader not set.")
        try:
            return self._flag_definitions[name]
        except KeyError:
            flag_definition = self._flag_loader(name)
            self._flag_definitions[name] = flag_definition
            return flag_definition

    def get_nutrient(self, name: str) -> "Nutrient":
        if self._nutrient_loader is None:
            raise RuntimeError("Nutrient loader not set.")
        try:
            return self._nutrients[name]
        except KeyError:
            nutrient = self._nutrient_loader(name)
            self._nutrients[name] = nutrient
            return nutrient

    def get_tag(self, name: str) -> "Tag":
        if name not in self._tags:
            self._tags = self._tag_graph_loader()
        return self._tags[name]

    def get_recipe(self, name: str) -> "Recipe":
        if self._recipe_loader is None:
            raise RuntimeError("Recipe loader not set.")
        try:
            return self._recipes[name]
        except KeyError:
            recipe = self._recipe_loader(name)
            self._recipes[name] = recipe
            return recipe

    def get_ingredient(self, name: str) -> "Ingredient":
        if self._ingredient_loader is None:
            raise RuntimeError("Ingredient loader not set.")
        try:
            return self._ingredients[name]
        except KeyError:
            ingredient = self._ingredient_loader(name)
            self._ingredients[name] = ingredient
            return ingredient

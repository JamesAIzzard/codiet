from typing import TYPE_CHECKING, TypedDict, Collection

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.utils.unique_dict import UniqueDict as UD
from codiet.utils.unique_dict import FrozenUniqueDict as FUD
from codiet.model.flags import HasFlags
from codiet.model.nutrients import HasNutrientQuantities
from codiet.model.calories import HasCalories

if TYPE_CHECKING:
    from codiet.model.quantities import UnitConversionService
    from codiet.model.nutrients import NutrientQuantity
    from codiet.model.flags import Flag, FlagFactory
    from codiet.model.time import TimeWindow, TimeWindowDTO
    from codiet.model.tags import Tag, TagDTO
    from codiet.model.ingredients import IngredientQuantity, IngredientQuantityDTO


class RecipeDTO(TypedDict):
    name: str
    use_as_ingredient: bool
    description: str | None
    instructions: list[str]
    ingredient_quantities: dict[str, "IngredientQuantityDTO"]
    serve_time_windows: Collection["TimeWindowDTO"]
    tags: Collection["TagDTO"]


class Recipe(HasCalories, HasNutrientQuantities, HasFlags):

    unit_conversion_service: "UnitConversionService"

    def __init__(
        self,
        name: str,
        use_as_ingredient: bool,
        description: str | None,
        instructions: list[str],
        ingredient_quantities: UD[str, "IngredientQuantity"],
        serve_time_windows: Collection["TimeWindow"],
        tags: Collection["Tag"],
        flag_factory: "FlagFactory",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._flag_factory = flag_factory

        self._name = name
        self._use_as_ingredient = use_as_ingredient
        self._description = description
        self._instructions = instructions
        self._ingredient_quantities = UD[str, "IngredientQuantity"](
            ingredient_quantities
        )
        self._serve_time_windows = MUC["TimeWindow"](serve_time_windows)
        self._tags = MUC["Tag"](tags)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if name is None or name.strip() == "":
            raise ValueError("Name cannot be None or empty.")
        self._name = name

    @property
    def use_as_ingredient(self) -> bool:
        return self._use_as_ingredient

    @use_as_ingredient.setter
    def use_as_ingredient(self, use_as_ingredient: bool) -> None:
        self._use_as_ingredient = use_as_ingredient

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, description: str | None) -> None:
        self._description = description

    @property
    def instructions(self) -> list[str]:
        return self._instructions

    @instructions.setter
    def instructions(self, instructions: list[str]) -> None:
        self._instructions = instructions

    @property
    def ingredient_quantities(self) -> IUC["IngredientQuantity"]:
        return IUC(self._ingredient_quantities.values())

    @property
    def serve_time_windows(self) -> IUC["TimeWindow"]:
        return IUC(self._serve_time_windows)

    @property
    def tags(self) -> IUC["Tag"]:
        return IUC(self._tags)
    
    @property
    def nutrient_quantities(self) -> FUD[str, "NutrientQuantity"]:
        nutrient_quantities = UD[str, "NutrientQuantity"]()

        for ingredient_quantity in self.ingredient_quantities:
            for nutrient_name, nutrient_quantity in ingredient_quantity.nutrient_quantities.items():
                if nutrient_name in nutrient_quantities:
                    nutrient_quantities[nutrient_name].quantity += nutrient_quantity.quantity
                else:
                    nutrient_quantities[nutrient_name] = nutrient_quantity

        return FUD(nutrient_quantities)

    @property
    def total_grams_in_definition(self) -> float:
        total_grams = 0

        for ingredient_quantity in self.ingredient_quantities:
            total_grams += self.unit_conversion_service.convert_quantity(
                quantity=ingredient_quantity.quantity,
                to_unit_name="gram",
                instance_unit_conversions=dict(ingredient_quantity.ingredient.unit_conversions)
            ).value
        
        return total_grams

    def get_flag(self, name: str) -> "Flag":
        flag = self._flag_factory.create_flag(name)

        if self.is_flag_none_on_any_ingredient(name):
            return flag.set_value(None)
        elif self.is_flag_false_on_any_ingredient(name):
            return flag.set_value(False)
        else:
            return flag.set_value(True)

    def is_flag_none_on_any_ingredient(self, name: str) -> bool:
        for ingredient_quantity in self.ingredient_quantities:
            if ingredient_quantity.ingredient.get_flag(name).value is None:
                return True
        return False

    def is_flag_false_on_any_ingredient(self, name: str) -> bool:
        for ingredient_quantity in self.ingredient_quantities:
            if ingredient_quantity.ingredient.get_flag(name).value is False:
                return True
        return False

    def add_ingredient_quantity(
        self, ingredient_quantity: "IngredientQuantity"
    ) -> "Recipe":
        if ingredient_quantity.ingredient.name in self._ingredient_quantities:
            raise ValueError(
                f"Ingredient quantity with name '{ingredient_quantity.ingredient.name}' already exists."
            )
        
        self._ingredient_quantities[ingredient_quantity.ingredient.name] = ingredient_quantity

        return self

    def remove_ingredient_quantity(
        self, ingredient_quantity: "IngredientQuantity"
    ) -> None:
        del self._ingredient_quantities[ingredient_quantity.ingredient.name]

    def add_serve_time_window(self, serve_time_window: "TimeWindow") -> None:
        self._serve_time_windows.add(serve_time_window)

    def remove_serve_time_window(self, serve_time_window: "TimeWindow") -> None:
        self._serve_time_windows.remove(serve_time_window)

    def add_tag(self, tag: "Tag") -> None:
        self._tags.add(tag)

    def remove_tag(self, tag: "Tag") -> None:
        self._tags.remove(tag)

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

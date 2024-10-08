from typing import TYPE_CHECKING, TypedDict, Collection

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.utils.unique_dict import UniqueDict
from codiet.model.flags import HasFlags

if TYPE_CHECKING:
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


class Recipe(HasFlags):

    def __init__(
        self,
        name: str,
        use_as_ingredient: bool,
        description: str | None,
        instructions: list[str],
        ingredient_quantities: UniqueDict[str, "IngredientQuantity"],
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
        self._ingredient_quantities = UniqueDict[str, "IngredientQuantity"](
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
        
        self._ingredient_quantities[ingredient_quantity.ingredient.name] = ingredient_quantity

        return self

    def get_ingredient_quantity_by_name(
        self, ingredient_name: str
    ) -> "IngredientQuantity":
        for ingredient_qty in self._ingredient_quantities:
            if ingredient_qty.ingredient.name.lower() == ingredient_name.lower():
                return ingredient_qty
        raise ValueError(
            f"Ingredient quantity with name '{ingredient_name}' not found."
        )

    def remove_ingredient_quantity(
        self, ingredient_quantity: "IngredientQuantity"
    ) -> None:
        self._ingredient_quantities.remove(ingredient_quantity)

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

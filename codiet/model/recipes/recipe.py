from typing import TYPE_CHECKING

from codiet.model import StoredEntity
from codiet.utils import MUC, IUC
from codiet.model.flags import Flag, HasFlags

if TYPE_CHECKING:
    from codiet.model.ingredients import IngredientQuantity
    from codiet.model.time import TimeWindow
    from codiet.model.tags import Tag


class Recipe(HasFlags, StoredEntity):

    def __init__(
        self,
        name: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._name = name
        self._use_as_ingredient: bool = False
        self._description: str | None = None
        self._instruction: str | None = None
        self._ingredient_quantities = MUC["IngredientQuantity"]()
        self._serve_time_windows = MUC["TimeWindow"]()
        self._tags = MUC["Tag"]()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Note:
            We don't do any uniqueness checks here. This is the responsibility of the
            database, and happens when we go to save the recipe.
        """
        # Raise an exception if the name is None or just whitespace
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
    def instructions(self) -> str | None:
        return self._instructions

    @instructions.setter
    def instructions(self, instructions: str | None) -> None:
        self._instructions = instructions

    @property
    def ingredient_quantities(self) -> IUC["IngredientQuantity"]:
        return IUC(self._ingredient_quantities)

    @property
    def serve_time_windows(self) -> IUC["TimeWindow"]:
        return IUC(self._serve_time_windows)

    @property
    def tags(self) -> IUC["Tag"]:
        return IUC(self._tags)

    def get_flag(self, name: str) -> Flag:
        flag = Flag(name)

        if self.is_flag_none_on_any_ingredient(name):
            return flag.set_value(None)
        elif self.is_flag_false_on_any_ingredient(name):
            return flag.set_value(False)
        else:
            return flag.set_value(True)

    def is_flag_none_on_any_ingredient(self, name: str) -> bool:
        for ingredient_quantity in self._ingredient_quantities:
            if ingredient_quantity.ingredient.get_flag(name).value is None:
                return True
        return False
    
    def is_flag_false_on_any_ingredient(self, name: str) -> bool:
        for ingredient_quantity in self._ingredient_quantities:
            if ingredient_quantity.ingredient.get_flag(name).value is False:
                return True
        return False

    def add_ingredient_quantity(
        self, ingredient_quantity: "IngredientQuantity"
    ) -> None:
        self._ingredient_quantities.add(ingredient_quantity)

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
        if self.id is None and self.name is None:
            raise ValueError("Recipe must have an ID or a name for comparison.")
        if self.id is None or other.id is None:
            return self.name == other.name
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, self.name))

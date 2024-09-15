"""Defines the Recipe class."""

from typing import TYPE_CHECKING, Collection

from codiet.db import StoredEntity
from codiet.utils import MUC, IUC

if TYPE_CHECKING:
    from codiet.model.ingredients import IngredientQuantity
    from codiet.model.time import TimeWindow
    from codiet.model.tags import Tag

class Recipe(StoredEntity):
    """Models a recipe."""

    def __init__(
        self,
        name: str,
        description: str | None = None,
        instructions: str | None = None,
        use_as_ingredient: bool = False,
        ingredient_quantities: Collection['IngredientQuantity']|None = None,
        serve_time_windows: Collection['TimeWindow']|None = None,
        tags: Collection['Tag']|None = None,
        *args,**kwargs,
    ):
        """Initialises the class."""
        super().__init__(*args, **kwargs)
        self._name = name
        self._use_as_ingredient = use_as_ingredient
        self._description = description
        self._instructions = instructions
        self._ingredient_quantities = MUC(ingredient_quantities) or MUC['IngredientQuantity']()
        self._serve_time_windows = MUC(serve_time_windows) or MUC['RecipeServeTimeWindow']()
        self._tags = MUC(tags) or MUC['RecipeTag']()

    @property
    def name(self) -> str:
        """Get the name of the recipe."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the recipe.
        Note:
            We don't do any uniqueness checks here. This is the responsibility of the
            database, and happens when we go to save the recipe.
        """
        # Raise an exception if the name is None or just whitespace
        if name is None or name.strip() == "":
            raise ValueError("Name cannot be None or empty.")
        self._name = name

    @property
    def use_as_ingredient(self) -> bool:
        """Get whether the recipe is used as an ingredient."""
        return self._use_as_ingredient

    @use_as_ingredient.setter
    def use_as_ingredient(self, use_as_ingredient: bool) -> None:
        """Set whether the recipe is used as an ingredient."""
        self._use_as_ingredient = use_as_ingredient

    @property
    def description(self) -> str | None:
        """Get the description of the recipe."""
        return self._description

    @description.setter
    def description(self, description: str | None) -> None:
        """Set the description of the recipe."""
        self._description = description

    @property
    def instructions(self) -> str | None:
        """Get the instructions for the recipe."""
        return self._instructions

    @instructions.setter
    def instructions(self, instructions: str | None) -> None:
        """Set the instructions for the recipe."""
        self._instructions = instructions

    @property
    def ingredient_quantities(self) -> IUC['IngredientQuantity']:
        """Returns the ingredient quantities for the recipe."""
        return IUC(self._ingredient_quantities)

    @property
    def serve_time_windows(self) -> IUC['TimeWindow']:
        """Returns the serve time windows for the recipe."""
        return IUC(self._serve_time_windows)

    @property
    def tags(self) -> IUC['Tag']:
        """Returns an immutable list of tags for the recipe."""
        return IUC(self._tags)

    def add_ingredient_quantity(self, ingredient_quantity: 'IngredientQuantity') -> None:
        """Add an ingredient to the recipe."""
        self._ingredient_quantities.add(ingredient_quantity)

    def get_ingredient_quantity_by_name(self, ingredient_name: str) -> 'IngredientQuantity':
        """Get an ingredient quantity by its name."""
        for ingredient_qty in self._ingredient_quantities:
            if ingredient_qty.ingredient.name == ingredient_name:
                return ingredient_qty
        raise ValueError(f"Ingredient quantity with name '{ingredient_name}' not found.")

    def remove_ingredient_quantity(self, ingredient_quantity: 'IngredientQuantity') -> None:
        """Remove an ingredient from the recipe."""
        for ingredient_qty in self._ingredient_quantities:
            if ingredient_qty == ingredient_quantity:
                self._ingredient_quantities.remove(ingredient_qty)
                break

    def add_serve_time_window(self, serve_time_window: 'TimeWindow') -> None:
        """Add a serve time window to the recipe."""
        self._serve_time_windows.add(serve_time_window)

    def remove_serve_time_window(self, serve_time_window: 'TimeWindow') -> None:
        """Remove a serve time window from the recipe."""
        for window in self._serve_time_windows:
            if window == serve_time_window:
                self._serve_time_windows.remove(window)
                break

    def add_tag(self, tag: 'Tag') -> None:
        """Add a tag to the recipe."""
        self._tags.add(tag)

    def __eq__(self, other):
        """Check if two recipes are equal."""
        if not isinstance(other, Recipe):
            return False
        if self.id is None and self.name is None:
            raise ValueError("Recipe must have an ID or a name for comparison.")
        if self.id is None or other.id is None:
            return self.name == other.name
        return self.id == other.id

    def __hash__(self):
        """Hash the recipe."""
        return hash((self.id, self.name))

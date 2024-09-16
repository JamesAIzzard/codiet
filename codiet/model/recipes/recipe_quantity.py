"""Defines the RecipeQuantity class."""

from typing import TYPE_CHECKING

from codiet.model.quantity.is_quantity import IsQuantity

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe
    from codiet.model.units import Unit


class RecipeQuantity(IsQuantity):
    """Models a recipe quantity."""

    def __init__(
        self,
        recipe: "Recipe",
        *args, **kwargs
    ):
        """Initialises the class."""
        super().__init__(*args, **kwargs)
        self._recipe = recipe

    @property
    def recipe(self) -> "Recipe":
        """Get the recipe."""
        return self._recipe


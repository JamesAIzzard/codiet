"""Defines the RecipeQuantity class."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe
    from codiet.model.units import Unit

class RecipeQuantity:
    """Models a recipe quantity."""

    def __init__(
        self,
        recipe: 'Recipe',
        quantity_unit: 'Unit',
        quantity: float
    ):
        """Initialises the class."""
        self._recipe = recipe
        self._quantity_unit = quantity_unit
        self._quantity = quantity

    @property
    def recipe(self) -> 'Recipe':
        """Get the recipe."""
        return self._recipe
    
    @property
    def quantity_unit(self) -> 'Unit':
        """Get the quantity unit."""
        return self._quantity_unit
    
    @property
    def quantity(self) -> float:
        """Get the quantity."""
        return self._quantity
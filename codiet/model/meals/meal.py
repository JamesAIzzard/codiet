"""Defines the meal class."""

from typing import TYPE_CHECKING, Collection

if TYPE_CHECKING:
    from codiet.model.recipes import RecipeQuantity

class Meal:
    """Models a meal.
    A meal is a collection of RecipeQuantity objects.
    """
    
    def __init__(
        self,
        recipe_quantities: Collection['RecipeQuantity']
    ):
        """Initialises the class."""
        self._recipe_quantities = recipe_quantities
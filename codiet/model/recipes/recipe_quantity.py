"""Defines the RecipeQuantity class."""

from typing import TYPE_CHECKING

from codiet.model.domain_service import UsesDomainService

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe
    from codiet.model.units import Unit


class RecipeQuantity(UsesDomainService):
    """Models a recipe quantity."""

    def __init__(
        self,
        recipe: "Recipe",
        quantity_unit: "Unit|None" = None,
        quantity: float | None = None,
        *args, **kwargs
    ):
        """Initialises the class."""
        super().__init__(*args, **kwargs)
        self._recipe = recipe
        self._quantity_unit = quantity_unit or self._domain_service.gram
        self._quantity = quantity

    @property
    def recipe(self) -> "Recipe":
        """Get the recipe."""
        return self._recipe

    @property
    def quantity_unit(self) -> "Unit|None":
        """Get the quantity unit."""
        return self._quantity_unit
    
    @quantity_unit.setter
    def quantity_unit(self, unit: "Unit") -> None:
        """Set the quantity unit."""
        # The unit should never be None, because we can
        # always default to grams.
        if unit is None:
            raise ValueError("The quantity unit cannot be None.")
        
        self._quantity_unit = unit

    @property
    def quantity(self) -> float | None:
        """Get the quantity."""
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity: float) -> None:
        """Set the quantity."""
        self._quantity = quantity

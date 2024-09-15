"""Defines the RecipeQuantity class."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model import DomainService
    from codiet.model.recipes import Recipe
    from codiet.model.units import Unit


class RecipeQuantity:
    """Models a recipe quantity."""

    _domain_service:'DomainService'

    @classmethod
    def setup(cls,domain_service:'DomainService') -> None:
        """Sets up the units and global unit conversions for the Recipe class."""
        cls._domain_service = domain_service

    def __init__(
        self,
        recipe: "Recipe",
        quantity_unit: "Unit|None" = None,
        quantity: float | None = None,
    ):
        """Initialises the class."""
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

    @property
    def quantity(self) -> float | None:
        """Get the quantity."""
        return self._quantity

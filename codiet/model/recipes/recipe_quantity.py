"""Defines the RecipeQuantity class."""

from typing import TYPE_CHECKING, Collection

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe
    from codiet.model.units import Unit, UnitConversion


class RecipeQuantity:
    """Models a recipe quantity."""

    _units: Collection["Unit"] | None = None
    _global_unit_conversions: Collection["UnitConversion"] | None = None

    @classmethod
    def setup(
        cls,
        units: Collection["Unit"],
        global_unit_conversions: Collection["UnitConversion"],
    ) -> None:
        """Sets up the units and global unit conversions for the Recipe class."""
        cls._units = units
        cls._global_unit_conversions = global_unit_conversions
        cls._gram = next(u for u in units if u.name == "gram")

    def __init__(
        self,
        recipe: "Recipe",
        quantity_unit: "Unit|None" = None,
        quantity: float | None = None,
    ):
        """Initialises the class."""
        self._recipe = recipe
        self._quantity_unit = quantity_unit or self._gram
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

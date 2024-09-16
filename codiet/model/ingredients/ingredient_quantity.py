from typing import TYPE_CHECKING

from codiet.db.stored_entity import StoredEntity
from codiet.model.quantity.is_quantity import IsQuantity

if TYPE_CHECKING:
    from codiet.model.ingredients.ingredient import Ingredient
    from codiet.model.units.unit import Unit


class IngredientQuantity(IsQuantity, StoredEntity):
    """Class to represent an ingredient quantity."""

    def __init__(
        self,
        ingredient: "Ingredient",
        qty_utol: float | None = None,
        qty_ltol: float | None = None,
        *args,
        **kwargs
    ):
        """Initialises the class."""
        super().__init__(*args, **kwargs)

        self._ingredient = ingredient

        self._upper_tol = qty_utol
        self._lower_tol = qty_ltol

    @property
    def ingredient(self) -> "Ingredient":
        """Get the ingredient."""
        return self._ingredient

    @property
    def qty_utol(self) -> float | None:
        """Get the upper tolerance."""
        return self._upper_tol

    @qty_utol.setter
    def qty_utol(self, qty_utol: float | None):
        """Set the upper tolerance."""
        self._upper_tol = qty_utol

    @property
    def qty_ltol(self) -> float | None:
        """Get the lower tolerance."""
        return self._lower_tol

    @qty_ltol.setter
    def qty_ltol(self, qty_ltol: float | None):
        """Set the lower tolerance."""
        self._lower_tol = qty_ltol

    def __eq__(self, other):
        if not isinstance(other, IngredientQuantity):
            return False
        return (self.ingredient) == (other.ingredient)

    def __hash__(self):
        return hash(self.ingredient)

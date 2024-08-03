from typing import TYPE_CHECKING

from codiet.models.units.unit_conversion import UnitConversion
if TYPE_CHECKING:
    from codiet.models.ingredients.ingredient import Ingredient

class IngredientUnitConversion(UnitConversion):
    """Models the conversion between two units assoicated with an ingredient."""

    def __init__(
        self, 
        ingredient: 'Ingredient',
        *args, **kwargs
    ):
        """Initialises the EntityUnitConversion object.
        Extends the UnitConversion object with an entity_id.
        """
        super().__init__(*args, **kwargs)

        self._ingredient = ingredient

    @property
    def ingredient(self) -> 'Ingredient':
        """Retrieves the ingredient associated with the conversion."""
        return self._ingredient

    def __eq__(self, other: object) -> bool:
        """Return True if the object is equal to another object."""
        if not isinstance(other, IngredientUnitConversion):
            return False
        return super().__eq__(other) and self._ingredient == other.ingredient

    def __hash__(self):
        return super().__hash__() + hash(self._ingredient)

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"EntityUnitConversion(from_unit={self.from_unit}, to_unit={self.to_unit}, ingredient={self.ingredient.name})"

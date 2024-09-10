from typing import TYPE_CHECKING

from .base_unit_conversion import BaseUnitConversion

if TYPE_CHECKING:
    from codiet.models.ingredients.ingredient import Ingredient

class IngredientUnitConversion(BaseUnitConversion):
    """Models a unit conversion associated with an ingredient.
    
    Extends BaseUnitConversion to include an ingredient object, and adds
    setters to allow the from and to unit quantities to be set.
    """

    def __init__(
        self, 
        ingredient: 'Ingredient',
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._ingredient = ingredient

    @property
    def ingredient(self) -> 'Ingredient':
        """Retrieves the ingredient associated with the conversion."""
        return self._ingredient
    
    @BaseUnitConversion.from_unit_qty.setter
    def from_unit_qty(self, value: float|None):
        """Sets the from unit."""
        self._from_unit_qty = value
    
    @BaseUnitConversion.to_unit_qty.setter
    def to_unit_qty(self, value: float|None):
        """Sets the to unit."""
        self._to_unit_qty = value

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

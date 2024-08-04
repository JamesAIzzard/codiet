from typing import TYPE_CHECKING

from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion

if TYPE_CHECKING:
    from codiet.models.ingredients.ingredient import Ingredient

class IngredientUnitConversion(UnitConversion):
    """Models the conversion between two units assoicated with an ingredient."""

    def __init__(
        self, 
        ingredient: 'Ingredient',
        from_unit_qty: float | None = None,
        to_unit_qty: float | None = None,
        *args, **kwargs
    ):
        """Initialises the EntityUnitConversion object.
        Extends the UnitConversion object with an entity_id.
        """

        super().__init__(
            from_unit_qty=from_unit_qty, # type: ignore # OK on this class
            to_unit_qty=to_unit_qty, # type: ignore # OK on this class
            *args, **kwargs
        )

        self._ingredient = ingredient

    @property
    def ingredient(self) -> 'Ingredient':
        """Retrieves the ingredient associated with the conversion."""
        return self._ingredient

    @property
    def from_unit_qty(self) -> float|None:
        """Returns the from unit."""
        return self._from_unit_qty
    
    @from_unit_qty.setter
    def from_unit_qty(self, value: float):
        """Sets the from unit."""
        self._from_unit_qty = value

    @property
    def to_unit_qty(self) -> float|None:
        """Returns the to unit."""
        return self._to_unit_qty
    
    @to_unit_qty.setter
    def to_unit_qty(self, value: float):
        """Sets the to unit."""
        self._to_unit_qty = value

    @property
    def is_defined(self) -> bool:
        """Returns True if the conversion is populated."""
        return self.from_unit_qty is not None and self.to_unit_qty is not None

    @property
    def ratio(self) -> float:
        """Returns the ratio between the two units."""
        if not self.is_defined:
            raise ValueError("The conversion is not fully defined.")
        return super().ratio
    
    def convert_quantity(self, qty: float) -> float:
        """Converts a quantity from the from unit to the to unit."""
        if not self.is_defined:
            raise ValueError("The conversion is not fully defined.")
        return super().convert_quantity(qty)
    
    def reverse_convert_quantity(self, qty: float) -> float:
        """Converts a quantity from the to unit to the from unit."""
        if not self.is_defined:
            raise ValueError("The conversion is not fully defined.")
        return super().reverse_convert_quantity(qty)

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

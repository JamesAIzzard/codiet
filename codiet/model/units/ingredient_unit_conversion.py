"""Defines class used to model a unit conversion associated
with an ingredient."""

from .unit_conversion import UnitConversion

class IngredientUnitConversion(UnitConversion):
    """Models a unit conversion associated with an ingredient.
    Extends a UnitConversion to include an ingredient ID.

    Note:
        IngredientUnitConversion instances get stored in a dedicated
        table, seperate from the (global) unit conversions. This seems
        a better approach than putting all unit conversions in one
        table and just leaving the ingredient ID empty for global ones.   
    """

    def __init__(
        self,
        ingredient_id: int,
        *args,
        **kwargs,
    ):
        """Initializes the class."""
        super().__init__(*args, **kwargs)

        self._ingredient_id = ingredient_id

    @property
    def ingredient_id(self) -> int:
        """Returns the ingredient ID."""
        return self._ingredient_id
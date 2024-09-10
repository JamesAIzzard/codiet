from .base_unit_conversion import BaseUnitConversion

class GlobalUnitConversion(BaseUnitConversion):
    """Models a global unit conversion.
    
    Extends BaseUnitConversion to enforce the presence of the from and to unit quantities.
    """

    def __init__(
            self, 
            from_unit_qty: float,
            to_unit_qty: float,
            *args, **kwargs
        ):
        """Initialise the UnitConversion object."""
        super().__init__(
            from_unit_qty=from_unit_qty,
            to_unit_qty=to_unit_qty,
            *args, **kwargs
        )

    @property
    def from_unit_qty(self) -> float:
        """Returns the quantity of the from unit."""
        value = super().from_unit_qty
        if value is None:
            raise ValueError("The from unit quantity is not defined.")
        return value

    @property
    def to_unit_qty(self) -> float:
        """Returns the quantity of the to unit."""
        value = super().to_unit_qty
        if value is None:
            raise ValueError("The to unit quantity is not defined.")
        return value
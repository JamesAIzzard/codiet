from codiet.db.stored_entity import StoredEntity
from .unit import Unit

class UnitConversion(StoredEntity):
    """Models the conversion between two units."""

    def __init__(
            self, 
            from_unit: Unit, 
            to_unit: Unit, 
            from_unit_qty: float|None = None,
            to_unit_qty: float|None = None,
            *args, **kwargs
        ):
        """Initialise the UnitConversion object."""
        super().__init__(*args, **kwargs)  

        # Raise an exception if the from and to units are identical
        if from_unit == to_unit:
            raise ValueError("The from and to units must be different.")

        self._from_unit = from_unit
        self._to_unit = to_unit
        self._from_unit_qty = from_unit_qty
        self._to_unit_qty = to_unit_qty

    @property
    def from_unit(self) -> Unit:
        """Returns the from unit."""
        return self._from_unit

    @property
    def to_unit(self) -> Unit:
        """Returns the to unit."""
        return self._to_unit

    @property
    def from_unit_qty(self) -> float|None:
        """Returns the quantity of the from unit."""
        return self._from_unit_qty
    
    @from_unit_qty.setter
    def from_unit_qty(self, value: float|None):
        """Sets the quantity of the from unit."""
        # Check the value is None or a positive number
        if value is not None and value <= 0:
            raise ValueError("from_unit_qty must be a positive number.")
        self._from_unit_qty = value

    @property
    def to_unit_qty(self) -> float|None:
        """Returns the quantity of the to unit."""
        return self._to_unit_qty
    
    @to_unit_qty.setter
    def to_unit_qty(self, value: float|None):
        """Sets the quantity of the to unit."""
        # Check the value is None or a positive number
        if value is not None and value <= 0:
            raise ValueError("to_unit_qty must be a positive number.")
        self._to_unit_qty = value

    @property
    def is_defined(self) -> bool:
        """Returns True if the conversion is populated."""
        return self.from_unit_qty is not None and self.to_unit_qty is not None

    @property
    def ratio(self) -> float:
        """Returns the ratio between the two units."""
        # Raise an exception if either id or qty is None
        if self.is_defined is False:
            raise ValueError("Both from_unit_qty and to_unit_qty must be set.")
        return self.to_unit_qty / self.from_unit_qty # type: ignore
    
    def convert_quantity(self, qty: float) -> float:
        """Converts a quantity from the from unit to the to unit."""
        # Raise an exception if either id or qty is None
        if self.is_defined is False:
            raise ValueError("Both from_unit_qty and to_unit_qty must be set.")
        return qty * self.ratio
    
    def reverse_convert_quantity(self, qty: float) -> float:
        """Converts a quantity from the to unit to the from unit."""
        # Raise an exception if either id or qty is None
        if self.is_defined is False:
            raise ValueError("Both from_unit_qty and to_unit_qty must be set.")
        return qty / self.ratio

    def __eq__(self, other):
        if not isinstance(other, UnitConversion):
            return False
        return (
            (self.from_unit == other.from_unit and self.to_unit == other.to_unit) or
            (self.from_unit == other.to_unit and self.to_unit == other.from_unit)
        )

    def __hash__(self):
        return hash(frozenset([self.from_unit, self.to_unit]))

    def __str__(self):
        return f"{self.from_unit}:{self.from_unit.type} -> {self.to_unit}:{self.to_unit.type}"
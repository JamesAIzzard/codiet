from codiet.db.stored_entity import StoredEntity
from codiet.models.units.unit import Unit

class BaseUnitConversion(StoredEntity):
    """Base class for unit conversions."""

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
        self._backwards = False

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

    @property
    def to_unit_qty(self) -> float|None:
        """Returns the quantity of the to unit."""
        return self._to_unit_qty

    @property
    def is_defined(self) -> bool:
        """Returns True if the conversion is populated."""
        return self.from_unit_qty is not None and self.to_unit_qty is not None

    @property
    def ratio(self) -> float:
        """Returns the ratio between the two units."""
        if self.is_defined:
            if self._backwards:
                return self.from_unit_qty / self.to_unit_qty # type: ignore # Checked by is_defined
            else:
                return self.to_unit_qty / self.from_unit_qty # type: ignore # Checked by is_defined
        raise ValueError("The conversion is not fully defined.")

    def reverse(self) -> None:
        """Reverses the conversion."""
        self._backwards = not self._backwards

    def convert_quantity(self, qty: float) -> float:
        """Converts a quantity from the from unit to the to unit."""
        if self.is_defined:
            return qty * self.ratio
        raise ValueError("The conversion is not fully defined.")
    
    def reverse_convert_quantity(self, qty: float) -> float:
        """Converts a quantity from the to unit to the from unit."""
        if self.is_defined:
            return qty / self.ratio
        raise ValueError("The conversion is not fully defined.")

    def __eq__(self, other):
        if not isinstance(other, BaseUnitConversion):
            return False
        return (
            (self.from_unit == other.from_unit and self.to_unit == other.to_unit) or
            (self.from_unit == other.to_unit and self.to_unit == other.from_unit)
        )

    def __hash__(self):
        return hash(frozenset([self.from_unit, self.to_unit]))

    def __str__(self):
        return f"{self.from_unit}:{self.from_unit.type} -> {self.to_unit}:{self.to_unit.type}"
class UnitConversion:
    """Models the conversion between two units."""

    def __init__(
            self, 
            id:int, 
            from_unit_id: int, 
            to_unit_id: int, 
            from_unit_qty: float|None = None,
            to_unit_qty: float|None = None,
        ):
        """
        Initialise the UnitConversion object.

        Args:
            id (int): The id of the conversion.
            from_unit_id (int): The id of the unit to convert from.
            to_unit_id (int): The id of the unit to convert to.
            from_unit_qty (float, optional): The quantity of the from unit. Defaults to None.
            to_unit_qty (float, optional): The quantity of the to unit. Defaults to None.
        """
        self.id = id
        self.from_unit_id = from_unit_id
        self.from_unit_qty = from_unit_qty
        self.to_unit_id = to_unit_id
        self.to_unit_qty = to_unit_qty

    def __eq__(self, other):
        if not isinstance(other, UnitConversion):
            return NotImplemented
        return (self.from_unit_id, self.to_unit_id) == (other.from_unit_id, other.to_unit_id) or \
               (self.from_unit_id, self.to_unit_id) == (other.to_unit_id, other.from_unit_id)

    @property
    def is_populated(self) -> bool:
        """Returns True if the conversion is populated."""
        return self.from_unit_qty is not None and self.to_unit_qty is not None

    @property
    def ratio(self) -> float:
        """Returns the ratio between the two units."""
        # Raise an exception if either id or qty is None
        if self.is_populated is False:
            raise ValueError("Both from_unit_qty and to_unit_qty must be set.")
        return self.to_unit_qty / self.from_unit_qty # type: ignore
    
    def convert_from_to(self, qty: float) -> float:
        """Converts a quantity from the from unit to the to unit."""
        # Raise an exception if either id or qty is None
        if self.is_populated is False:
            raise ValueError("Both from_unit_qty and to_unit_qty must be set.")
        return qty * self.ratio
    
    def convert_to_from(self, qty: float) -> float:
        """Converts a quantity from the to unit to the from unit."""
        # Raise an exception if either id or qty is None
        if self.is_populated is False:
            raise ValueError("Both from_unit_qty and to_unit_qty must be set.")
        return qty / self.ratio

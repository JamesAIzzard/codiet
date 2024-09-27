from codiet.db.stored_entity import StoredEntity
from codiet.model.quantities import Quantity

class UnitConversion(StoredEntity):

    def __init__(
            self,
            quantities: tuple[Quantity, Quantity], 
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)  

        # Raise an exception if the from and to units are identical
        if quantities[0].unit == quantities[1].unit:
            raise ValueError("The from and to units are identical.")
        
        self._quantities = quantities

    @property
    def quantities(self) -> tuple[Quantity, Quantity]:
        return self._quantities

    @property
    def is_defined(self) -> bool:
        return self.quantities[0].is_defined and self.quantities[1].is_defined

    @property
    def _forwards_ratio(self) -> float:
        if not self.is_defined:
            raise ValueError("The quantities are not defined.")
        return self.quantities[1].value / self.quantities[0].value # type: ignore
    
    @property
    def _reverse_ratio(self) -> float:
        return 1 / self._forwards_ratio

    def has_unit(self, unit) -> bool:
        return unit in [qty.unit for qty in self.quantities]

    def convert_from(self, quantity: Quantity) -> Quantity:
        # The conversion must be defined to do any converting
        if not self.is_defined:
            raise ValueError("The quantities are not defined.")

        # The unit to convert from must be in one of the quantity units
        if not self.has_unit(quantity.unit):
            raise ValueError("The unit to convert from is not in the quantities.")
        
        # Determine the direction of conversion and call the appropriate method
        if quantity.unit == self.quantities[0].unit:
            return self._convert_forward(quantity)
        else:
            return self._convert_reverse(quantity)

    def _convert_forward(self, quantity: Quantity) -> Quantity:
        converted_value = quantity.value * self._forwards_ratio # type: ignore
        converted_unit = self.quantities[1].unit
        return Quantity(value=converted_value, unit=converted_unit)

    def _convert_reverse(self, quantity: Quantity) -> Quantity:
        converted_value = quantity.value * self._reverse_ratio # type: ignore
        converted_unit = self.quantities[0].unit
        return Quantity(value=converted_value, unit=converted_unit)

    def __eq__(self, other):
        if not isinstance(other, UnitConversion):
            return False
        # The unit conversions are considered equal if their quantities are equal.
        return (self.quantities[0] == other.quantities[0])

    def __hash__(self):
        return hash(self.quantities)

    def __str__(self):
        return f"{self.quantities[0]} -> {self.quantities[1]}"
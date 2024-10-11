from typing import TYPE_CHECKING, TypedDict

from codiet.model.quantities import Quantity

if TYPE_CHECKING:
    from codiet.model.quantities import Quantity, QuantityDTO


class UnitConversionDTO(TypedDict):
    from_quantity: "QuantityDTO"
    to_quantity: "QuantityDTO"


class UnitConversion:

    def __init__(self, 
            from_quantity: Quantity, 
            to_quantity: Quantity,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)

        if from_quantity == to_quantity:
            raise ValueError("The from and to quantities are identical.")

        self._from_quantity = from_quantity
        self._to_quantity = to_quantity

    @property
    def quantities(self) -> tuple[Quantity, Quantity]:
        return (self._from_quantity, self._to_quantity)

    @property
    def unit_names(self) -> tuple[str, str]:
        return (
            self.quantities[0].unit.name,
            self.quantities[1].unit.name
        )

    @property
    def is_defined(self) -> bool:
        return self.quantities[0].is_defined and self.quantities[1].is_defined

    @property
    def _forwards_ratio(self) -> float:
        if not self.is_defined:
            raise ValueError("The quantities are not defined.")
        return self.quantities[1].value / self.quantities[0].value  # type: ignore

    @property
    def _reverse_ratio(self) -> float:
        return 1 / self._forwards_ratio

    def get_definition_value(self, unit_name: str) -> float:
        if not self.is_defined:
            raise ValueError("The quantities are not defined.")
        if unit_name == self.quantities[0].unit.name:
            return self.quantities[0].value
        elif unit_name == self.quantities[1].unit.name:
            return self.quantities[1].value
        else:
            raise ValueError("The unit name is not in the quantities.")

    def has_unit(self, unit) -> bool:
        return unit in [qty.unit for qty in self.quantities]

    # TODO: Are these methods necessary? Doesn't UnitConversionService handle this?
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
        converted_value = quantity.value * self._forwards_ratio  # type: ignore
        converted_unit = self.quantities[1].unit
        return Quantity(value=converted_value, unit=converted_unit)

    def _convert_reverse(self, quantity: Quantity) -> Quantity:
        converted_value = quantity.value * self._reverse_ratio  # type: ignore
        converted_unit = self.quantities[0].unit
        return Quantity(value=converted_value, unit=converted_unit)

    def __eq__(self, other):
        if not isinstance(other, UnitConversion):
            return False
        # The unit conversions are considered equal if their quantities are equal.
        return self.quantities[0] == other.quantities[0]

    def __hash__(self):
        return hash(self.quantities)

    def __str__(self):
        return f"{self.quantities[0]} -> {self.quantities[1]}"

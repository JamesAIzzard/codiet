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

    def has_unit(self, unit) -> bool:
        return unit in [qty.unit for qty in self.quantities]

    def __eq__(self, other):
        if not isinstance(other, UnitConversion):
            return False
        # The unit conversions are considered equal if their quantities are equal.
        return self.quantities[0] == other.quantities[0]

    def __hash__(self):
        return hash(self.quantities)

    def __str__(self):
        return f"{self.quantities[0]} -> {self.quantities[1]}"

from typing import TYPE_CHECKING, TypedDict

from codiet.utils.unique_dict import FrozenUniqueDict as FUD

if TYPE_CHECKING:
    from codiet.model.quantities import Quantity, QuantityDTO


class UnitConversionDTO(TypedDict):
    from_quantity: "QuantityDTO"
    to_quantity: "QuantityDTO"


class UnitConversion:

    def __init__(self, 
            from_quantity: "Quantity", 
            to_quantity: "Quantity",
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)

        if from_quantity == to_quantity:
            raise ValueError("The from and to quantities are identical.")

        self._from_quantity = from_quantity
        self._to_quantity = to_quantity

    @property
    def quantities(self) -> FUD[str, "Quantity"]:
        return FUD[str, "Quantity"]({
            self._from_quantity.unit.name: self._from_quantity,
            self._to_quantity.unit.name: self._to_quantity
        })

    @property
    def unit_names(self) -> tuple[str, str]:
        return tuple(self.quantities.keys())

    @property
    def is_defined(self) -> bool:
        for qty in self.quantities.values():
            if not qty.is_defined:
                return False
        return True

    @property
    def _forwards_ratio(self) -> float:
        if not self.is_defined:
            raise ValueError("The quantities are not defined.")
        return self.quantities[1].value / self.quantities[0].value  # type: ignore

    @property
    def _reverse_ratio(self) -> float:
        return 1 / self._forwards_ratio

    def __eq__(self, other):
        if not isinstance(other, UnitConversion):
            return False
        return self.quantities == other.quantities

    def __hash__(self):
        return hash(self.quantities)

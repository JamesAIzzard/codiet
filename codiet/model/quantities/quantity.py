from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversionService

class QuantityDTO(TypedDict):
    unit_name: str
    value: float | None

class Quantity:

    def __init__(self,
            unit: "Unit",
            value: float|None=None,
            *args, **kwargs
    ):
        
        super().__init__(*args, **kwargs)

        self._unit = unit
        self._value = value

    @property
    def unit(self) -> "Unit":
        return self._unit

    @property
    def value(self) -> float:
        if self._value is None:
            raise TypeError("Value not set")
        return self._value

    @property
    def is_defined(self) -> bool:
        return self._value is not None
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Quantity):
            return False
        return self.unit == value.unit and self.value == value.value
    
    def __hash__(self) -> int:
        if not self.is_defined:
            value = None
        else:
            value = self.value
        return hash((self.unit, value))
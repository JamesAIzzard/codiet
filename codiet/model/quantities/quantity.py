from typing import TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversionService

class QuantityDTO(TypedDict):
    unit_name: str
    value: float | None

class Quantity:

    _initialised = False
    unit_conversion_service: "UnitConversionService"

    def __init__(self,
            unit: "Unit",
            value: float|None=None,
            *args, **kwargs
    ):
        if not self._initialised:
            raise RuntimeError("Quantity class not initialised. Call initialise() first.")
        
        super().__init__(*args, **kwargs)

        self._unit = unit
        self._value = value

    @classmethod
    def initialise(cls, unit_conversion_service: "UnitConversionService"):
        cls.unit_conversion_service = unit_conversion_service
        cls._initialised = True

    @property
    def unit(self) -> "Unit":
        return self._unit
    
    @unit.setter
    def unit(self, unit:"Unit") -> None:
        self._unit = unit

    @property
    def value(self) -> float:
        if self._value is None:
            raise TypeError("Value not set")
        return self._value

    @property
    def value_in_grams(self) -> float:
        return self.unit_conversion_service.convert_quantity(
            quantity=self,
            to_unit_name="gram"
        ).value

    @property
    def is_defined(self) -> bool:
        return self._value is not None

    def set_value(self, value: float|None) -> 'Quantity':
        self._value = value

        return self
    
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
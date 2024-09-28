from typing import TYPE_CHECKING

from codiet.model import SingletonRegistry

if TYPE_CHECKING:
    from codiet.model.quantities.unit import Unit

class Quantity():

    @classmethod
    def from_unit_name(cls, unit_name: str, value: float|None=None) -> 'Quantity':
        unit = SingletonRegistry().get_unit(unit_name)
        return cls(unit, value)    
    
    @classmethod
    def from_unit(cls, unit: 'Unit', value: float|None=None) -> 'Quantity':
        return cls(unit, value)

    def __init__(self,
            unit: 'Unit|None'=None,
            value: float|None=None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._unit = unit or SingletonRegistry().get_unit("gram")
        self._value = value

    @property
    def unit(self) -> 'Unit':
        return self._unit

    @property
    def value(self) -> float:
        if self._value is None:
            raise TypeError("Value not set")
        return self._value

    @property
    def is_defined(self) -> bool:
        return self._value is not None

    def set_unit(self, unit: 'Unit') -> 'Quantity':
        self._unit = unit
        return self
    
    def set_unit_from_name(self, unit_name: str) -> 'Quantity':
        self._unit = SingletonRegistry().get_unit(unit_name)
        return self
    
    def set_value(self, value: float|None) -> 'Quantity':
        self._value = value

        return self
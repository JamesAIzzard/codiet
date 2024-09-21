from typing import TYPE_CHECKING

from codiet.model.domain_service import UsesDomainService

if TYPE_CHECKING:
    from codiet.model.quantities.unit import Unit

class Quantity(UsesDomainService):

    @classmethod
    def from_unit_name(cls, unit_name: str, value: float|None=None) -> 'Quantity':
        unit = cls.get_domain_service().get_unit(unit_name)
        return cls(unit, value)    

    def __init__(self, unit: 'Unit|str|None'=None, value: float|None=None):
        super().__init__()
        
        if isinstance(unit, str):
            unit = self.domain_service.get_unit(unit)

        self._unit = unit or self.domain_service.gram
        self._value = value

    @property
    def unit(self) -> 'Unit':
        return self._unit

    @property
    def value(self) -> float|None:
        return self._value

    def set_unit(self, unit: 'Unit|str') -> 'Quantity':
        if isinstance(unit, str):
            unit = self.get_domain_service().get_unit(unit)

        self._unit = unit
        return self
    
    def set_value(self, value: float|None) -> 'Quantity':
        self._value = value

        return self
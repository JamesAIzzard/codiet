"""Defines the domain service for the model."""

from typing import Collection, TYPE_CHECKING

from codiet.utils import IUC

if TYPE_CHECKING:
    from codiet.model.units import Unit, UnitConversion

class DomainService:
    """The domain service for the model."""

    def __init__(
        self, 
        global_units: Collection['Unit'], 
        global_unit_conversions: Collection['UnitConversion']
    ) -> None:
        self._global_units = global_units
        self._global_unit_conversions = global_unit_conversions
        self._gram = self.get_unit_by_name("gram")

    @property
    def global_units(self) -> IUC['Unit']:
        return IUC(self._global_units)

    @property
    def gram(self) -> 'Unit':
        return self._gram

    @property
    def global_unit_conversions(self) -> IUC['UnitConversion']:
        return IUC(self._global_unit_conversions)
    
    def get_unit_by_name(self, name: str) -> 'Unit':
        """Returns a unit by name."""
        for unit in self._global_units:
            if unit.name == name:
                return unit
        raise ValueError(f"Unit '{name}' not found.")
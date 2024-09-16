"""Defines the domain service for the model."""

from typing import Collection, TYPE_CHECKING

from codiet.utils import IUC

if TYPE_CHECKING:
    from codiet.model.units import Unit, UnitConversion
    from codiet.model.flags import Flag
    from codiet.model.nutrients import Nutrient
    from codiet.model.ingredients import Ingredient

class DomainService:
    """The domain service for the model."""

    def __init__(
        self, 
        global_units: Collection['Unit'], 
        global_unit_conversions: Collection['UnitConversion'],
        global_flags: Collection['Flag'],
        global_nutrients: Collection['Nutrient'],
    ) -> None:
        self._global_units = global_units
        self._global_unit_conversions = global_unit_conversions
        self._global_flags = global_flags
        self._global_nutrients = global_nutrients

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
    
    @property
    def global_flags(self) -> IUC['Flag']:
        return IUC(self._global_flags)

    @property
    def global_nutrients(self) -> IUC['Nutrient']:
        return IUC(self._global_nutrients)

    def get_unit_by_name(self, name: str) -> 'Unit':
        """Returns a unit by name."""
        for unit in self.global_units:
            if unit.name == name:
                return unit
        raise ValueError(f"Unit '{name}' not found.")
    
    def get_flag_by_name(self, name: str) -> 'Flag':
        """Returns a flag by name."""
        for flag in self.global_flags:
            if flag.name == name:
                return flag
        raise ValueError(f"Flag '{name}' not found.")
    
    def get_flags_by_names(self, names: list[str]) -> IUC['Flag']:
        """Returns flags by name."""
        return IUC([self.get_flag_by_name(name) for name in names])
    
    def get_nutrient_by_name(self, name: str) -> 'Nutrient':
        """Returns a nutrient by name."""
        for nutrient in self.global_nutrients:
            if nutrient.name == name:
                return nutrient
        raise ValueError(f"Nutrient '{name}' not found.")
    
    def get_nutrients_by_names(self, names: list[str]) -> IUC['Nutrient']:
        """Returns nutrients by name."""
        return IUC([self.get_nutrient_by_name(name) for name in names])
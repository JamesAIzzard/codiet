"""Defines the Quantity class."""

from typing import TYPE_CHECKING

from codiet.model.domain_service import UsesDomainService

if TYPE_CHECKING:
    from codiet.model.quantities.unit import Unit

class Quantity(UsesDomainService):
    """Models a quantity of a unit."""

    def __init__(self, unit: 'Unit|None'=None, value: float|None=None):
        """Initialise the Quantity object."""
        super().__init__()
        self._unit = unit
        self._value = value

    @property
    def unit(self) -> 'Unit':
        """Returns the unit of the quantity."""
        if self._unit is None:
            self._unit = self.domain_service.gram
        return self._unit

    @property
    def value(self) -> float|None:
        """Returns the quantity."""
        return self._value
    
    @value.setter
    def value(self, value: float|None):
        """Sets the quantity."""
        self._value = value
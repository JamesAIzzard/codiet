"""Defines the class implementing functionality to model an object with a measured quantity."""

from typing import TYPE_CHECKING

from codiet.model.domain_service import UsesDomainService

if TYPE_CHECKING:
    from codiet.model.units import Unit

class IsQuantity(UsesDomainService):
    def __init__(
            self,
            quantity_unit: 'Unit | None' = None,
            quantity_value: float | None = None,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)
        self._quantity_unit = quantity_unit or self.domain_service.gram
        self._quantity_value = quantity_value

    @property
    def quantity_unit(self) -> 'Unit | None':
        """Returns the quantity unit."""
        return self._quantity_unit
    
    @quantity_unit.setter
    def quantity_unit(self, value: 'Unit') -> None:
        """Sets the quantity unit."""
        self._quantity_unit = value

    @property
    def quantity_value(self) -> float | None:
        """Returns the quantity value."""
        return self._quantity_value
    
    @quantity_value.setter
    def quantity_value(self, value: float) -> None:
        """Sets the quantity value."""
        self._quantity_value = value

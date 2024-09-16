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
        self._quantity_unit = quantity_unit or self._domain_service.gram
        self._quantity_value = quantity_value

    @property
    def quantity_unit(self) -> 'Unit | None':
        """Returns the quantity unit."""
        return self._quantity_unit
    
    @property
    def quantity_value(self) -> float | None:
        """Returns the quantity value."""
        return self._quantity_value

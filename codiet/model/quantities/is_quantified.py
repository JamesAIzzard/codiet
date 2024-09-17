"""Defines the class implementing functionality to model an object with a measured quantity."""

from typing import TYPE_CHECKING

from codiet.model.domain_service import UsesDomainService

if TYPE_CHECKING:
    from codiet.model.quantities import Quantity

class IsQuantified(UsesDomainService):
    def __init__(self, quantity: 'Quantity|None' = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quantity = quantity

    @property
    def quantity(self) -> 'Quantity|None':
        """Return the quantity."""
        return self._quantity

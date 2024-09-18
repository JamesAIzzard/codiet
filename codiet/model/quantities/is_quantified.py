"""Defines the class implementing functionality to model an object with a measured quantity."""

from codiet.model.domain_service import UsesDomainService
from .quantity import Quantity

class IsQuantified(UsesDomainService):
    def __init__(self, quantity: 'Quantity|None' = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quantity = quantity or Quantity(self.domain_service.gram)

    @property
    def quantity(self) -> 'Quantity':
        """Return the quantity."""
        return self._quantity

from codiet.model.domain_service import UsesDomainService
from .quantity import Quantity

class IsQuantified(UsesDomainService):
    def __init__(self, quantity: 'Quantity|None' = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quantity = quantity or Quantity()

    @property
    def quantity(self) -> 'Quantity':
        """Return the quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: 'Quantity'):
        """Set the quantity."""
        self._quantity = value
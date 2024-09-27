from .quantity import Quantity

class IsQuantified:

    def __init__(self, quantity: 'Quantity|None'=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._quantity = quantity or Quantity()

    @property
    def quantity(self) -> 'Quantity':
        return self._quantity

    @quantity.setter
    def quantity(self, value: 'Quantity'):
        self._quantity = value
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.quantities import Quantity


class IsQuantified:

    def __init__(self, quantity: "Quantity", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._quantity = quantity

    @property
    def quantity(self) -> "Quantity":
        return self._quantity

    @quantity.setter
    def quantity(self, value: "Quantity"):
        self._quantity = value

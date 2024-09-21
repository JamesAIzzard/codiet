from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.quantities import Quantity

class QuantityCost:
    def __init__(self, quantity: 'Quantity', cost:float|None = None):
        self._quantity = quantity
        self._cost = cost

    @property
    def quantity(self) -> 'Quantity':
        return self._quantity
    
    @property
    def cost(self) -> float|None:
        return self._cost
    
    @cost.setter
    def cost(self, value: float) -> None:
        if value < 0:
            raise ValueError("Cost cannot be negative.")

        self._cost = value
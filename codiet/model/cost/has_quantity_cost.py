from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.cost import QuantityCost

class HasQuantityCost:
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._quantity_cost: 'QuantityCost|None' = None

    @property
    def quantity_cost(self) -> 'QuantityCost':
        if self._quantity_cost is None:
            raise ValueError("Quantity cost is not set.")
        return self._quantity_cost
    

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from . import HasQuantityCost

if TYPE_CHECKING:
    from . import QuantityCost

class HasSettableQuantityCost(HasQuantityCost, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def set_quantity_cost(self, value: 'QuantityCost') -> None:
        raise NotImplementedError

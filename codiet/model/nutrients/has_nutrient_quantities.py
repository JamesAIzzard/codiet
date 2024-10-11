from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from codiet.utils.unique_dict import FrozenUniqueDict as FUD
    from codiet.model.nutrients import NutrientQuantity

class HasNutrientQuantities(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    @abstractmethod
    def nutrient_quantities(self) -> "FUD[str, NutrientQuantity]":
        raise NotImplementedError
    
    def get_nutrient_quantity(self, name: str) -> 'NutrientQuantity':
        return self.nutrient_quantities[name]
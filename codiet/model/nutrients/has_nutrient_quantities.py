from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from codiet.exceptions.nutrients import NutrientUndefinedError

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
    
    def is_nutrient_present(self, nutrient_name:str) -> bool:
        if nutrient_name not in self.nutrient_quantities:
            raise NutrientUndefinedError(nutrient_name)
        if self.nutrient_quantities[nutrient_name].quantity.value == 0:
            return False
        return True

    def get_nutrient_quantity(self, name: str) -> 'NutrientQuantity':
        return self.nutrient_quantities[name]
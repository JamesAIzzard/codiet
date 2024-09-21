from typing import TYPE_CHECKING, Collection
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from codiet.model.nutrients import NutrientQuantity

class HasNutrientQuantities(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    @abstractmethod
    def nutrient_quantities(self) -> Collection['NutrientQuantity']:
        raise NotImplementedError
    
    def get_nutrient_quantity(self, name: str) -> 'NutrientQuantity':
        for nutrient_quantity in self.nutrient_quantities:
            if nutrient_quantity.nutrient.name == name:
                return nutrient_quantity
            
        raise ValueError(f"Nutrient {name} not found.")
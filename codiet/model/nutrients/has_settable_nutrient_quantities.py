from typing import TYPE_CHECKING, Collection
from abc import ABC, abstractmethod

from codiet.model.nutrients import HasNutrientQuantities

class HasSettableNutrientQuantities(HasNutrientQuantities):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    
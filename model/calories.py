from typing import Union
from abc import ABC, abstractmethod

from model.ingredient import Ingredient
from model.meal import Meal

class HasCalories(ABC):
    """Base class for objects which have calories when assigned a quantity."""
    @property
    @abstractmethod
    def calories_per_gram(self) -> float:
        raise NotImplementedError


def get_calories(subject: Union[Ingredient, Meal], quantity_in_g: float) -> float:
    """Returns number of calories as float:"""
    raise NotImplementedError

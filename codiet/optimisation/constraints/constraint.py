from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe

class Constraint(ABC):
    
    @abstractmethod
    def is_satisfied_by(self, recipe:'Recipe') -> bool:
        raise NotImplementedError
    
    def filter(self, potential_recipes: list['Recipe']) -> list['Recipe']:
        return [recipe for recipe in potential_recipes if self.is_satisfied_by(recipe)]
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe

class Constraint(ABC):
    
    @abstractmethod
    def is_satisfied(self, recipe:'Recipe') -> bool:
        raise NotImplementedError
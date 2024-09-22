from abc import ABC, abstractmethod
from typing import Collection, TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe
    from codiet.optimisation.constraints import Constraint

class RecipeSource(ABC):

    @property
    @abstractmethod
    def recipes(self) -> Collection['Recipe']:
        pass

    @abstractmethod
    def add_constraint(self, constraint:'Constraint') -> 'RecipeSource':
        raise NotImplementedError

    def get_recipes(self) -> Collection['Recipe']:
        return self.recipes
    
    def add_constraints(self, constraints:Collection['Constraint']) -> 'RecipeSource':
        recipe_source = self
        for constraint in constraints:
            recipe_source = recipe_source.add_constraint(constraint)
        return self
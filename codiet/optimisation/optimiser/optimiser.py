from typing import Collection, TYPE_CHECKING

from codiet.utils import IUC
from codiet.model import DietPlan

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe
    from codiet.optimisation.algorithms import Algorithm
    from codiet.optimisation.constraints import Constraint

class Optimiser:

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._recipe_source: Collection['Recipe']|None = None
        self._constraints: Collection['Constraint']|None = None
        self._algorithm: 'Algorithm'|None = None

    def solve(self) -> IUC['DietPlan']:
        return IUC([DietPlan()])
    
    def set_recipe_source(self, recipes:Collection['Recipe']) -> 'Optimiser':
        return self

    def set_constraints(self, constraints:Collection['Constraint']) -> 'Optimiser':
        return self

    def set_algorithm(self, algorithm:'Algorithm') -> 'Optimiser':
        return self
        
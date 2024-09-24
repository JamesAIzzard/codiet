from typing import Collection, TYPE_CHECKING

from codiet.utils import IUC
from codiet.optimisation.problems import Problem
from codiet.optimisation.solutions import Solution
from codiet.optimisation.algorithms import Algorithm

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe
    from codiet.optimisation.algorithms import Algorithm
    from codiet.optimisation.constraints import Constraint

class Optimiser:

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._recipe_source: Collection['Recipe']|None = None
        self._constraints: Collection['Constraint']|None = None
        self._algorithm: 'Algorithm|None' = None

    def solve(self, problem:'Problem') -> IUC['Solution']:
        return IUC([Solution()])
    
    def set_recipe_source(self, recipes:Collection['Recipe']) -> 'Optimiser':
        return self

    def add_problem(self, problem:'Problem') -> 'Optimiser':
        return self

    def set_algorithm(self, algorithm:'Algorithm') -> 'Optimiser':
        return self
        
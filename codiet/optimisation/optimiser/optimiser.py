from typing import Collection, TYPE_CHECKING

from codiet.optimisation.problems import DietProblem
from codiet.optimisation.solutions import DietSolution
from codiet.optimisation.algorithms import Algorithm

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe
    from codiet.optimisation.algorithms import Algorithm

class Optimiser:

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._recipe_source: Collection['Recipe']|None = None
        self._algorithm: 'Algorithm|None' = None

    def solve(self, problem:'DietProblem') -> 'DietSolution':
        return DietSolution(problem)
    
    def set_recipe_source(self, recipes:Collection['Recipe']) -> 'Optimiser':
        return self

    def set_algorithm(self, algorithm:'Algorithm') -> 'Optimiser':
        return self
        
from typing import Collection, TYPE_CHECKING

from codiet.utils import IUC
from codiet.optimisation.problems import DietProblem
from codiet.optimisation.solutions import DietSolution
from codiet.optimisation.algorithms import Algorithm
from codiet.model.recipes import RecipeQuantity

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe
    from codiet.optimisation.algorithms import Algorithm

class Optimiser:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._recipe_source: Collection['Recipe']|None = None
        self._algorithm: 'Algorithm|None' = None

    def solve(self, problem: 'DietProblem') -> IUC['DietSolution']:
        solution = DietSolution(problem)

        for leaf_address in solution.leaf_addresses:
            recipe_quantity = RecipeQuantity("dummy_recipe")
            
            solution.add_recipe_quantity_to_address(leaf_address, recipe_quantity)

        return IUC([solution])

    def set_recipe_source(self, recipes: Collection['Recipe']) -> 'Optimiser':
        self._recipe_source = recipes
        return self

    def set_algorithm(self, algorithm: 'Algorithm') -> 'Optimiser':
        self._algorithm = algorithm
        return self
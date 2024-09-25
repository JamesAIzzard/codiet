from typing import TYPE_CHECKING
from collections import UserDict

if TYPE_CHECKING:
    from codiet.optimisation.problems import DietProblem
    from codiet.model.recipes import Recipe

class DietSolution(UserDict):
    def __init__(self, problem: 'DietProblem'):
        super().__init__()
        for key, subproblem in problem.items():
            if subproblem.is_leaf():
                self.data[key] = None  # Will be replaced with a Recipe instance
            else:
                self.data[key] = DietSolution(subproblem)

    def __setitem__(self, key, value):
        raise AttributeError("DietSolution is immutable")

    def _set_recipe(self, path: list[str], recipe: 'Recipe'):
        node = self
        for key in path[:-1]:
            node = node[key]
        node.data[path[-1]] = recipe
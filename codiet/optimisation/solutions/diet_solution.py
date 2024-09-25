from typing import TYPE_CHECKING
from collections import UserDict

if TYPE_CHECKING:
    from codiet.optimisation.problems import DietProblem
    from codiet.model.recipes import Recipe

class DietSolution(UserDict):
    def __init__(self, problem: 'DietProblem', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._name = problem.name
        self._recipe: 'Recipe|None' = None

        self.data:dict[str, 'DietSolution'] = {k: DietSolution(v) for k, v in problem.items()}

    @property
    def name(self) -> str:
        return self._name

    @property
    def recipe(self) -> 'Recipe':
        if not self.is_leaf:
            raise AttributeError("Non-leaf nodes of DietSolution do not have recipes")
        elif self._recipe is None:
            raise AttributeError("No recipe set for this node")
        return self._recipe

    @recipe.setter
    def recipe(self, recipe: 'Recipe'):
        if self.is_leaf:
            self._recipe = recipe
        else:
            raise AttributeError("Non-leaf nodes of DietSolution do not have recipes")

    @property
    def is_leaf(self) -> bool:
        return len(self.data) == 0

    def __setitem__(self, key:str, value: 'DietSolution'):
        if not self[key].is_leaf:
            raise AttributeError("Non-leaf nodes of DietSolution are immutable")
        self.data[key] = value

    def __getitem__(self, key: str) -> 'DietSolution':
        return self.data[key]
from typing import TYPE_CHECKING
from codiet.optimisation.diet_structure import DietStructure

if TYPE_CHECKING:
    from codiet.optimisation.problems import DietProblem
    from codiet.model.recipes import RecipeQuantity

class DietSolution(DietStructure):
    def __init__(self, problem: 'DietProblem', *args, **kwargs):
        super().__init__(problem.name, *args, **kwargs)

        self._recipe: 'RecipeQuantity|None' = None

        self.data = {k: DietSolution(v) for k, v in problem.items()}

    @property
    def recipe_quantity(self) -> 'RecipeQuantity':
        if not self.is_leaf:
            raise AttributeError("Non-leaf nodes of DietSolution do not have recipes")
        elif self._recipe is None:
            raise AttributeError("No recipe set for this node")
        return self._recipe

    @recipe_quantity.setter
    def recipe_quantity(self, recipe: 'RecipeQuantity'):
        if self.is_leaf:
            self._recipe = recipe
        else:
            raise AttributeError("Non-leaf nodes of DietSolution do not have recipes")

    def add_recipe_quantity_to_address(self, address: list[str], recipe: 'RecipeQuantity') -> 'DietSolution':
        if not address:
            raise ValueError("Address cannot be empty")
        
        current_node = self
        for node_name in address[1:]:  # Skip the first name as it's the root node name
            if node_name not in current_node.data:
                raise KeyError(f"Invalid address: {address}")
            current_node = current_node.data[node_name]
        
        if not current_node.is_leaf:
            raise ValueError(f"Cannot add recipe to non-leaf node: {address}")
        
        current_node.recipe_quantity = recipe
        return self

    def __setitem__(self, key:str, value: 'DietSolution'):
        if key not in self.data:
            raise KeyError(f"Key '{key}' not found in DietSolution")
        self.data[key] = value

    def __getitem__(self, key: str) -> 'DietSolution':
        return self.data[key]
from typing import Collection, TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe, RecipeFactory
    from codiet.optimisation.algorithms import Algorithm
    from codiet.optimisation import DietStructure


class Optimiser:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self._recipe_factory: "RecipeFactory"
        self._algorithm: "Algorithm|None" = None

    def solve(self, diet_structure: "DietStructure") -> "DietStructure":
        i = 5
        for recipe_node in diet_structure.recipe_nodes:
            for i in range(5):
                solution = self._recipe_factory.create_recipe(
                    name="porridge"
                )
                recipe_node.add_solution(solution, i)
        return diet_structure

    def set_recipe_source(self, recipes: Collection["Recipe"]) -> "Optimiser":
        self._recipe_source = recipes
        return self

    def set_algorithm(self, algorithm: "Algorithm") -> "Optimiser":
        self._algorithm = algorithm
        return self

from typing import Collection, TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.data import DatabaseService
    from codiet.model.recipes import Recipe
    from codiet.optimisation.algorithms import Algorithm
    from codiet.optimisation import DietStructure


class Optimiser:

    algorithm: "Algorithm"
    database_service: "DatabaseService"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def initialise(cls, database_service: "DatabaseService") -> None:
        cls.database_service = database_service

    def solve(self, diet_structure: "DietStructure") -> "DietStructure":
        i = 5
        for recipe_node in diet_structure.recipe_nodes:
            for i in range(5):
                solution = self.database_service.read_recipe(
                    recipe_name="apple_pie"
                )
                recipe_node.add_solution(solution, i)
        return diet_structure

    def set_recipe_source(self, recipes: Collection["Recipe"]) -> "Optimiser":
        self._recipe_source = recipes
        return self

    def set_algorithm(self, algorithm: "Algorithm") -> "Optimiser":
        self._algorithm = algorithm
        return self

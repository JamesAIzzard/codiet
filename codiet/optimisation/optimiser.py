from typing import Collection, TYPE_CHECKING
import random

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
        for recipe_node in diet_structure.solution_nodes():
            potential_recipes:list["Recipe"] = list(self.database_service.read_all_recipes().values())

            for constraint in diet_structure.get_constraints(recipe_node.address):
                potential_recipes = constraint.filter(potential_recipes)
                if len(potential_recipes) == 0:
                    raise ValueError(f"No recipes satisfy constraint {constraint} for node {recipe_node.address}")

            # Randomly selelct a recipe for the solution
            solution = random.choice(potential_recipes)
            recipe_node.add_solution(solution, 1)

        return diet_structure

    def set_recipe_source(self, recipes: Collection["Recipe"]) -> "Optimiser":
        self._recipe_source = recipes
        return self

    def set_algorithm(self, algorithm: "Algorithm") -> "Optimiser":
        self._algorithm = algorithm
        return self

from typing import Collection

from codiet.tests import BaseCodietTest
from codiet.data import DatabaseService
from codiet.optimisation import Optimiser
from codiet.optimisation.constraints import FlagConstraint
from codiet.optimisation.problems import DietProblem
from codiet.optimisation.solutions import DietSolution
from codiet.model.recipes import RecipeQuantity

class BaseOptimiserTest(BaseCodietTest):
    pass

class TestConstructor(BaseOptimiserTest):
    
    def test_can_create_optimiser(self):
        optimiser = Optimiser()

        self.assertIsInstance(optimiser, Optimiser)

class TestSolve(BaseOptimiserTest):
    
    def test_returns_collection_of_solutions(self):
        optimiser = Optimiser()

        breakfast = DietProblem("Breakfast")

        results = optimiser.solve(breakfast)

        self.assertIsInstance(results, Collection)
        self.assertTrue(all(isinstance(result, DietSolution) for result in results))

    def test_each_diet_solution_is_populated_with_recipes(self):
        optimiser = Optimiser()

        breakfast_problem = DietProblem("Breakfast", {
            "Drink": {},
            "Main": {}
        })

        results = optimiser.solve(breakfast_problem)

        for breakfast_solution in results:
            self.assertIsInstance(breakfast_solution["Breakfast"]["Drink"].recipe_quantity, RecipeQuantity)
            self.assertIsInstance(breakfast_solution["Breakfast"]["Main"].recipe_quantity, RecipeQuantity)

    
    def test_all_diet_plans_satisfy_recipe_problem_flag_constraints(self):
        optimiser = Optimiser()

        breakfast_problem = DietProblem("Breakfast")
        breakfast_problem.add_constraint(FlagConstraint("vegan", True))
        breakfast_problem.add_constraint(FlagConstraint("gluten_free", True))

        results = optimiser.solve(breakfast_problem)

        for breakfast_solution in results:
            solution_recipe = breakfast_solution.recipe_quantity.recipe
            self.assertEqual(DatabaseService.read_recipe_flag(solution_recipe, "vegan"), True)
            self.assertEqual(DatabaseService.read_recipe_flag(solution_recipe, "gluten_free"), True)
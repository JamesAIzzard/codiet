from typing import Collection
from unittest import skip

from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.optimiser import OptimiserTestFixtures
from codiet.tests.fixtures.recipes import RecipeTestFixtures
from codiet.tests.fixtures.constraints import ConstraintTestFixtures
from codiet.optimisation.optimiser import Optimiser
from codiet.optimisation.constraints import FlagConstraint
from codiet.optimisation.problems import DietProblem
from codiet.optimisation.solutions import DietSolution

class BaseOptimiserTest(BaseCodietTest):
    def setUp(self) -> None:
        super().setUp()
        self.constraint_fixtures = ConstraintTestFixtures.get_instance()
        self.recipe_fixtures = RecipeTestFixtures.get_instance()
        self.optimiser_fixtures = OptimiserTestFixtures.get_instance()

class TestConstructor(BaseOptimiserTest):
    
    def test_can_create_optimiser(self):
        optimiser = Optimiser()

        self.assertIsInstance(optimiser, Optimiser)

class TestSolve(BaseOptimiserTest):
    
    def test_returns_collection_of_solutions(self):
        optimiser = self.optimiser_fixtures.deterministic_optimiser

        breakfast = DietProblem("Breakfast")

        results = optimiser.solve(breakfast)

        self.assertIsInstance(results, Collection)
        self.assertTrue(all(isinstance(result, DietSolution) for result in results))

    
    def test_all_diet_plans_satisfy_recipe_problem_flag_constraints(self):
        optimiser = self.optimiser_fixtures.deterministic_optimiser

        breakfast_problem = DietProblem("Breakfast")
        breakfast_problem.add_constraint(FlagConstraint("vegan", True))
        breakfast_problem.add_constraint(FlagConstraint("gluten_free", True))

        results = optimiser.solve(breakfast_problem)

        for breakfast_solution in results:
            self.assertTrue(breakfast_solution.recipe.get_flag("vegan").value)
            self.assertTrue(breakfast_solution.recipe.get_flag("gluten_free").value)
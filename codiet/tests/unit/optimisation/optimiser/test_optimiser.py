from typing import Collection
from unittest import skip

from codiet.tests import BaseCodietTest
from codiet.tests.fixtures import ConstraintTestFixtures, RecipeTestFixtures, OptimiserTestFixtures
from codiet.optimisation.optimiser import Optimiser
from codiet.optimisation.constraints import FlagConstraint, TagConstraint
from codiet.optimisation.problems import Problem
from codiet.optimisation.solutions import Solution

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

        problem = Problem({
            "Breakfast": {
                "Drink": {},
                "Main": {}
            }
        })

        problem["Breakfast"].add_constraint(FlagConstraint('vegan', True))
        problem["Breakfast"].add_constraint(FlagConstraint('gluten_free', True))
        problem["Breakfast"]["Drink"].add_constraint(TagConstraint("drink"))
        problem["Breakfast"]["Main"].add_constraint(TagConstraint("cereal"))

        results = optimiser.solve(problem)

        self.assertIsInstance(results, Collection)
        for item in results:
            self.assertIsInstance(item, Solution)
    
    @skip("Not yet implemented")
    def test_all_diet_plans_satisfy_recipe_problem_flag_constraints(self):
        optimiser = self.optimiser_fixtures.deterministic_optimiser

        problem = Problem({"Breakfast": {}})
        problem.add_constraint(FlagConstraint("vegan", True))
        problem.add_constraint(FlagConstraint("gluten_free", True))

        results = optimiser.solve(problem)

        for solution in results:
            self.assertTrue(solution.get_flag('vegan').value)
            self.assertTrue(solution.get_flag('gluten_free').value)
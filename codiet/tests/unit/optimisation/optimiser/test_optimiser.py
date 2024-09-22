from typing import Collection

from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.constraints import ConstraintTestFixtures
from codiet.tests.fixtures.recipes import RecipeTestFixtures
from codiet.optimisation.optimiser import Optimiser
from codiet.optimisation import algorithms
from codiet.model.diet_plan import DietPlan

class BaseOptimiserTest(BaseCodietTest):
    def setUp(self) -> None:
        super().setUp()
        self.constraint_fixtures = ConstraintTestFixtures.get_instance()
        self.recipe_fixtures = RecipeTestFixtures.get_instance()

class TestConstructor(BaseOptimiserTest):
    
    def test_can_create_optimiser(self):
        optimiser = Optimiser()

        self.assertIsInstance(optimiser, Optimiser)

class TestSolve(BaseOptimiserTest):
    
    def test_returns_collection_of_diet_plans(self):
        constraints = [
            self.constraint_fixtures.create_flag_constraint('vegan', True),
            self.constraint_fixtures.create_flag_constraint('gluten_free', True),
        ]

        optimiser = Optimiser()
        optimiser.set_recipe_source(self.recipe_fixtures.recipes.values())
        optimiser.set_constraints(constraints)
        optimiser.set_algorithm(algorithms.Deterministic())

        results = optimiser.solve()

        self.assertIsInstance(results, Collection)
        for item in results:
            self.assertIsInstance(item, DietPlan)
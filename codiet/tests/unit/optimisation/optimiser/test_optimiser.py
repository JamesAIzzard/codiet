from codiet.tests import BaseCodietTest
from codiet.tests.fixtures import OptimiserFixtures
from codiet.data import DatabaseService
from codiet.optimisation import Optimiser
from codiet.optimisation import DietStructure
from codiet.optimisation.constraints import FlagConstraint
from codiet.model.recipes import RecipeQuantity

class BaseOptimiserTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()

        self.optimiser = Optimiser()
        self.optimiser._recipe_factory = self.recipe_factory

class TestConstructor(BaseOptimiserTest):
    
    def test_can_create_optimiser(self):
        optimiser = Optimiser()

        self.assertIsInstance(optimiser, Optimiser)

class TestSolve(BaseOptimiserTest):
    
    def test_structure_gets_collection_of_solutions(self):

        monday = DietStructure(OptimiserFixtures().monday_structure)

        for node in monday.recipe_nodes:
            self.assertFalse(node.has_recipe_solutions)

        self.optimiser.solve(monday)

        for node in monday.recipe_nodes:
            self.assertTrue(node.has_recipe_solutions)

    
    def test_all_diet_plans_satisfy_flag_constraints(self):

        monday = DietStructure(OptimiserFixtures().monday_structure)

        vegan_constraint = FlagConstraint("vegan", True)

        monday = self.optimiser.solve(monday)

        for recipe_node in monday.recipe_nodes:
            for recipe_quantity in recipe_node.solutions.values():
                self.assertTrue(recipe_quantity.get_flag_value("vegan"))
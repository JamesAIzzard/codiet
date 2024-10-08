from codiet.tests import BaseCodietTest
from codiet.tests.fixtures import OptimiserFixtures
from codiet.optimisation import DietStructure
from codiet.optimisation.constraints import FlagConstraint

class BaseOptimiserTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()

        self.optimiser_fixtures = OptimiserFixtures()

class TestSolve(BaseOptimiserTest):
    
    def test_structure_gets_collection_of_solutions(self):

        monday = DietStructure(self.optimiser_fixtures.monday_structure)

        for node in monday.recipe_nodes:
            self.assertFalse(node.has_recipe_solutions)

        optimiser = self.optimiser_factory.create_optimiser()
        optimiser.solve(monday)

        for node in monday.recipe_nodes:
            self.assertTrue(node.has_recipe_solutions)

    
    def test_all_diet_plans_satisfy_flag_constraints(self):

        monday = DietStructure(OptimiserFixtures().monday_structure)
        optimiser = self.optimiser_factory.create_optimiser()

        vegan_constraint = FlagConstraint("vegan", True)

        monday.get_node(()).add_constraint(vegan_constraint)

        monday = optimiser.solve(monday)

        for recipe_node in monday.recipe_nodes:
            for recipe_quantity in recipe_node.solutions.values():
                self.assertTrue(recipe_quantity.get_flag("vegetarian").value)
                self.assertFalse(recipe_quantity.get_flag("vegan").value)
                self.assertFalse(recipe_quantity.get_flag("gluten_free").value)
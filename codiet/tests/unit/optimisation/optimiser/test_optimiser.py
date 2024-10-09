from codiet.tests import BaseCodietTest
from codiet.tests.fixtures import OptimiserFixtures
from codiet.optimisation import DietStructure
from codiet.optimisation.constraints import FlagConstraint, CalorieConstraint

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

    def test_diet_plans_satisfy_calorie_constraints(self):

        two_day = DietStructure({
            "Monday": {
                "Breakfast": {"Main": {}},
                "Lunch": {"Main": {}},
                "Dinner": {"Main": {}}
            },
            "Tuesday": {
                "Breakfast": {"Main": {}},
                "Lunch": {"Main": {}},
                "Dinner": {"Main": {}}
            },
        })

        two_day.get_node(("Monday",)).add_constraint(CalorieConstraint(2000))
        two_day.get_node(("Tuesday",)).add_constraint(CalorieConstraint(3000))

        optimiser = self.optimiser_factory.create_optimiser()

        two_day = optimiser.solve(two_day)

        self.assertAlmostEqual(two_day.get_node(("Monday",)).solutions[0].calories, 2000, delta=1)
        self.assertAlmostEqual(two_day.get_node(("Tuesday",)).solutions[0].calories, 2000, delta=1)
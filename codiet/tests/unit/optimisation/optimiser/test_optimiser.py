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

        for node in monday.solution_nodes():
            self.assertFalse(node.has_recipe_solutions)

        optimiser = self.optimiser_factory.create_optimiser()
        optimiser.solve(monday)

        for node in monday.solution_nodes():
            self.assertTrue(node.has_recipe_solutions)

    def test_all_solutions_satisfy_constraints_to_entire_tree(self):

        monday = DietStructure(OptimiserFixtures().monday_structure)
        optimiser = self.optimiser_factory.create_optimiser()

        constraints = [
            FlagConstraint("vegan", True),
            FlagConstraint("vegetarian", True)
        ]

        for constraint in constraints:
            monday.add_constraint(
                address=(),
                constraint=constraint
            )

        monday = optimiser.solve(monday)

        for recipe_node in monday.solution_nodes():
            for recipe in recipe_node.solutions.values():
                self.assertTrue(recipe.get_flag("vegetarian").value)
                self.assertTrue(recipe.get_flag("vegan").value)

    def test_diet_plans_satisfy_calorie_constraints(self):

        two_day = DietStructure(
            {
                "Monday": {
                    "Breakfast": {"Main": {}},
                    "Lunch": {"Main": {}},
                    "Dinner": {"Main": {}},
                },
                "Tuesday": {
                    "Breakfast": {"Main": {}},
                    "Lunch": {"Main": {}},
                    "Dinner": {"Main": {}},
                },
            }
        )

        two_day.add_constraint(
            address=("Monday",),
            constraint=CalorieConstraint(2000)
        )
        two_day.add_constraint(
            address=("Tuesday",),
            constraint=CalorieConstraint(3000)
        )

        optimiser = self.optimiser_factory.create_optimiser()

        two_day = optimiser.solve(two_day)

        monday_cals_total = 0
        for solution in two_day.get_child_solutions(("Monday",)):
            monday_cals_total += solution.calories
        self.assertAlmostEqual(monday_cals_total, 2000, places=1)

        tuesday_cals_total = 0
        for solution in two_day.get_child_solutions(("Tuesday",)):
            tuesday_cals_total += solution.calories
        self.assertAlmostEqual(tuesday_cals_total, 3000, places=1)

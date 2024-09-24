from codiet.tests import BaseCodietTest
from codiet.optimisation.problems import Problem
from codiet.optimisation.constraints import FlagConstraint

class BaseProblemTest(BaseCodietTest):
    pass

class TestConstructor(BaseProblemTest):

    def test_can_create_problem(self):
        problem = Problem()

        self.assertIsInstance(problem, Problem)

    def test_can_create_problem_with_dict(self):
        problem = Problem({
            "Breakfast": {
                "Drink": {},
                "Main": {}
            }
        })

        self.assertIsInstance(problem, Problem)
        self.assertTrue(len(problem["Breakfast"]) == 2)

    def test_child_nodes_are_problem_instances(self):
        problem = Problem({
            "Breakfast": {
                "Drink": {},
                "Main": {}
            }
        })

        self.assertIsInstance(problem["Breakfast"], Problem)
        self.assertIsInstance(problem["Breakfast"]["Drink"], Problem)
        self.assertIsInstance(problem["Breakfast"]["Main"], Problem)

class TestAddConstraint(BaseProblemTest):

    def test_can_add_constraint(self):
        problem = Problem()

        self.assertEqual(len(problem.constraints), 0)

        problem.add_constraint(FlagConstraint('vegan', True))

        self.assertEqual(len(problem.constraints), 1)

    def test_can_add_constraint_to_specific_meal(self):
        problem = Problem({
            "Breakfast": {
                "Drink": {},
                "Main": {}
            }
        })

        self.assertEqual(len(problem["Breakfast"].constraints), 0)

        problem["Breakfast"].add_constraint(FlagConstraint('vegan', True))
        problem["Breakfast"]["Drink"].add_constraint(FlagConstraint('vegan', True))

        self.assertEqual(len(problem["Breakfast"].constraints), 1)
        self.assertEqual(len(problem["Breakfast"]["Drink"].constraints), 1)
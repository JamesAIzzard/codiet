from codiet.tests import BaseCodietTest
from codiet.optimisation.problems import DietProblem
from codiet.optimisation.constraints import FlagConstraint

class BaseDietProblemTest(BaseCodietTest):
    pass

class TestConstructor(BaseDietProblemTest):

    def test_can_create_problem(self):
        breakfast = DietProblem("Breakfast")

        self.assertIsInstance(breakfast, DietProblem)

    def test_can_create_problem_with_structure(self):
        breakfast = DietProblem("Breakfast", {
            "Drink": {},
            "Main": {}
        })

        self.assertIsInstance(breakfast, DietProblem)
        self.assertTrue(len(breakfast) == 2)

class TestAddSubproblem(BaseDietProblemTest):
    
    def test_can_add_subproblem(self):
        monday = DietProblem("Monday")

        self.assertEqual(len(monday), 0)

        monday.add_subproblem("Breakfast")
        monday.add_subproblem("Lunch")

        self.assertEqual(len(monday), 2)

    def test_can_add_subproblem_with_structure(self):
        monday = DietProblem("Monday")

        monday.add_subproblem("Breakfast", {
            "Drink": {},
            "Main": {}
        })

        self.assertEqual(len(monday), 1)
        self.assertTrue(len(monday["Breakfast"]) == 2)

class TestAddConstraint(BaseDietProblemTest):

    def test_can_add_constraint(self):
        breakfast = DietProblem("Breakfast")

        self.assertEqual(len(breakfast.constraints), 0)

        breakfast.add_constraint(FlagConstraint('vegan', True))

        self.assertEqual(len(breakfast.constraints), 1)

    def test_can_add_constraint_to_specific_meal(self):
        breakfast = DietProblem("Breakfast", {
            "Drink": {},
            "Main": {}
        })

        self.assertEqual(len(breakfast.constraints), 0)

        breakfast.add_constraint(FlagConstraint('vegan', True))
        breakfast["Drink"].add_constraint(FlagConstraint('vegan', True))

        self.assertEqual(len(breakfast.constraints), 1)
        self.assertEqual(len(breakfast["Drink"].constraints), 1)
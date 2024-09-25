from codiet.tests import BaseCodietTest

from codiet.optimisation.solutions import DietSolution
from codiet.optimisation.problems import DietProblem
from codiet.model.recipes import Recipe

class BaseDietSolutionTest(BaseCodietTest):
    pass

class TestConstructor(BaseDietSolutionTest):
        
        def test_can_create_solution(self):
            solution = DietSolution(DietProblem("Breakfast"))
    
            self.assertIsInstance(solution, DietSolution)

        def test_structure_matches_problem(self):
            problem = DietProblem("Breakfast", {
                "Drink": {},
                "Main": {}
            })

            solution = DietSolution(problem)

            self.assertEqual(len(solution), 2)
            self.assertTrue("Drink" in solution)
            self.assertTrue("Main" in solution)

class TestRecipeGetter(BaseDietSolutionTest):
    
    def test_can_access_recipe(self):
        breakfast_problem = DietProblem("Breakfast", {
            "Drink": {},
            "Main": {}
        })

        breakfast_solution = DietSolution(breakfast_problem)
        breakfast_solution["Drink"].recipe = Recipe("Coffee")

        self.assertIsInstance(breakfast_solution["Drink"].recipe, Recipe)

    def test_can_access_deep_recipe(self):
        monday_problem = DietProblem("Monday", {
            "Breakfast": {
                "Drink": {},
                "Main": {}
            },
            "Lunch": {
                "Drink": {},
                "Main": {}
            }
        })

        monday_solution = DietSolution(monday_problem)
        monday_solution["Breakfast"]["Drink"].recipe = Recipe("Coffee")

        self.assertIsInstance(monday_solution["Breakfast"]["Drink"].recipe, Recipe)
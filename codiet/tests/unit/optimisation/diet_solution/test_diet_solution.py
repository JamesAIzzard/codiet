from codiet.tests import BaseCodietTest

from codiet.optimisation.solutions import DietSolution
from codiet.optimisation.problems import DietProblem

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
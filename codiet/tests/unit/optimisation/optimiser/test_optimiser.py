from codiet.tests import BaseCodietTest
from codiet.tests.fixtures import OptimiserFixtures
from codiet.data import DatabaseService
from codiet.optimisation import Optimiser
from codiet.optimisation import DietStructure
from codiet.optimisation.constraints import FlagConstraint
from codiet.model.recipes import RecipeQuantity

class BaseOptimiserTest(BaseCodietTest):
    pass

class TestConstructor(BaseOptimiserTest):
    
    def test_can_create_optimiser(self):
        optimiser = Optimiser()

        self.assertIsInstance(optimiser, Optimiser)

class TestSolve(BaseOptimiserTest):
    
    def test_structure_gets_collection_of_solutions(self):
        optimiser = Optimiser()

        monday = DietStructure(OptimiserFixtures().monday_structure)

        for node in monday.recipe_nodes:
            self.assertFalse(node.has_recipe_solutions())

        optimiser.solve(monday)

        for node in monday.recipe_nodes:
            self.assertTrue(node.has_recipe_solutions())

    def test_each_diet_solution_is_populated_with_recipes(self):
        optimiser = Optimiser()

        breakfast_problem = DietProblem("Breakfast", {
            "Drink": {},
            "Main": {}
        })

        results = optimiser.solve(breakfast_problem)

        for breakfast_solution in results:
            self.assertIsInstance(breakfast_solution["Breakfast"]["Drink"].recipe_quantity, RecipeQuantity)
            self.assertIsInstance(breakfast_solution["Breakfast"]["Main"].recipe_quantity, RecipeQuantity)

    
    def test_all_diet_plans_satisfy_recipe_problem_flag_constraints(self):
        optimiser = Optimiser()

        breakfast_problem = DietProblem("Breakfast")
        breakfast_problem.add_constraint(FlagConstraint("vegan", True))
        breakfast_problem.add_constraint(FlagConstraint("gluten_free", True))

        results = optimiser.solve(breakfast_problem)

        for breakfast_solution in results:
            solution_recipe = breakfast_solution.recipe_quantity.recipe
            self.assertEqual(DatabaseService.read_recipe_flag(solution_recipe, "vegan"), True)
            self.assertEqual(DatabaseService.read_recipe_flag(solution_recipe, "gluten_free"), True)
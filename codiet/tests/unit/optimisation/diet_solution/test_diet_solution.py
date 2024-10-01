from codiet.tests import BaseCodietTest

from codiet.optimisation.solutions import DietSolution
from codiet.optimisation.problems import DietProblem
from codiet.model.recipes import RecipeQuantity
from codiet.model.quantities import Quantity

class BaseDietSolutionTest(BaseCodietTest):
    def setUp(self) -> None:
        super().setUp()

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
        breakfast_solution["Drink"].recipe_quantity = RecipeQuantity(
            recipe="coffee",
            quantity=Quantity(
                value=500,
                unit="millilitre"
            )
        )

        self.assertIsInstance(breakfast_solution["Drink"].recipe_quantity, RecipeQuantity)
        self.assertIs(breakfast_solution["Drink"].recipe_quantity.recipe, "coffee")

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
        monday_solution["Breakfast"]["Drink"].recipe_quantity = RecipeQuantity(
            recipe="coffee",
            quantity=Quantity(
                value=500,
                unit="millilitre"
            )
        )

        self.assertIsInstance(monday_solution["Breakfast"]["Drink"].recipe_quantity, RecipeQuantity)
        self.assertIs(monday_solution["Breakfast"]["Drink"].recipe_quantity.recipe, "coffee")

class TestAddRecipeQuantityToAddress(BaseDietSolutionTest):
    
    def test_can_add_recipe_to_address(self):
        monday_problem = DietProblem("Monday", {
            "Breakfast": {
                "Drink": {},
                "Main": {}
            }
        })

        monday_solution = DietSolution(monday_problem)
        recipe_quantity = RecipeQuantity(
            recipe="coffee",
            quantity=Quantity(
                value=500,
                unit="millilitre"
            )
        )

        monday_solution.add_recipe_quantity_to_address(["Monday", "Breakfast", "Drink"], recipe_quantity)

        self.assertIsInstance(monday_solution["Breakfast"]["Drink"].recipe_quantity, RecipeQuantity)
        self.assertIs(monday_solution["Breakfast"]["Drink"].recipe_quantity.recipe, "coffee")

    def test_exception_if_address_is_not_leaf(self):
        monday_problem = DietProblem("Monday", {
            "Breakfast": {
                "Drink": {},
                "Main": {}
            }
        })

        monday_solution = DietSolution(monday_problem)
        recipe_quantity = RecipeQuantity(
            recipe="coffee",
            quantity=Quantity(
                value=500,
                unit="millilitre"
            )
        )

        with self.assertRaises(ValueError):
            monday_solution.add_recipe_quantity_to_address(["Monday", "Breakfast"], recipe_quantity)
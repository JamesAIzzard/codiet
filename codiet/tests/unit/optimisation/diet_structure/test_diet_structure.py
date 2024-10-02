from codiet.tests import BaseCodietTest
from codiet.optimisation import DietStructure
from codiet.optimisation.constraints import FlagConstraint
from codiet.optimisation.goals import MinimiseNutrientGoal
from codiet.model.recipes import RecipeQuantity

class BaseDietStructureTest(BaseCodietTest):
    def setUp(self) -> None:
        self.monday_outline = {
            "Monday": {
                "Breakfast": {"Drink": {}, "Main": {}},
                "Lunch": {"Drink": {}, "Main": {}},
                "Dinner": {"Drink": {}, "Main": {}}
            }
        }

class TestConstructor(BaseDietStructureTest):
    
    def test_can_create_diet_structure(self):
        structure = DietStructure()

        self.assertIsInstance(structure, DietStructure)

    def test_can_create_with_structure(self):
        structure = DietStructure(self.monday_outline)

        self.assertIsInstance(structure, DietStructure)

class TestAddConstraint(BaseDietStructureTest):

    def test_can_add_constraint_to_root(self):
        structure = DietStructure(self.monday_outline)
        constraint = FlagConstraint("vegan", True)
        structure.add_constraint(constraint, [])

        self.assertIn(constraint, structure([]).constraints)

    def test_can_add_constraint_to_node(self):
        structure = DietStructure(self.monday_outline)
        constraint = FlagConstraint("vegan", True)
        structure.add_constraint(constraint, ["Monday", "Breakfast"])

        self.assertIn(constraint, structure(["Monday", "Breakfast"]).constraints)

class TestAddGoal(BaseDietStructureTest):

    def test_can_add_goal_to_root(self):
        structure = DietStructure(self.monday_outline)
        goal = MinimiseNutrientGoal("carbohydrate")
        structure.add_goal(goal, [])

        self.assertIn(goal, structure([]).goals)

    def test_can_add_goal_to_node(self):
        structure = DietStructure(self.monday_outline)
        goal = goal = MinimiseNutrientGoal("carbohydrate")
        structure.add_goal(goal, ["Monday", "Breakfast"])

        self.assertIn(goal, structure(["Monday", "Breakfast"]).goals)

class TestAddSolution(BaseDietStructureTest):
    
    def test_exception_if_node_is_not_leaf(self):
        structure = DietStructure(self.monday_outline)

        with self.assertRaises(ValueError):
            mug_of_coffee = RecipeQuantity(0.5, "L", "coffee")
            structure.add_solution(
                solution=mug_of_coffee,
                solution_set_id=1,
                path=["Monday"]
            )

    def test_can_add_solution_to_node(self):
        structure = DietStructure(self.monday_outline)
        mug_of_coffee = RecipeQuantity(0.5, "L", "coffee")
        structure.add_solution(
            solution=mug_of_coffee,
            solution_set_id=1,
            path=["Monday", "Breakfast", "Drink"]
        )

        self.assertEqual(
            structure(["Monday", "Breakfast", "Drink"]).solutions[1],
            mug_of_coffee
        )

class TestRecipeNodes(BaseDietStructureTest):
    
    def test_can_get_recipe_nodes(self):
        structure = DietStructure(self.monday_outline)

        self.assertTrue(len(structure.recipe_nodes) == 6)

        self.assertTrue(("Breakfast", "Drink") in structure.recipe_nodes.keys())
        self.assertTrue(("Breakfast", "Main") in structure.recipe_nodes.keys())
        self.assertTrue(("Lunch", "Drink") in structure.recipe_nodes.keys())
        self.assertTrue(("Lunch", "Main") in structure.recipe_nodes.keys())
        self.assertTrue(("Dinner", "Drink") in structure.recipe_nodes.keys())
        self.assertTrue(("Dinner", "Main") in structure.recipe_nodes.keys())

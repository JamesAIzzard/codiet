from codiet.tests import BaseCodietTest

from codiet.tests.fixtures import OptimiserFixtures
from codiet.optimisation import DietStructure
from codiet.optimisation.constraints import FlagConstraint
from codiet.optimisation.goals import MinimiseNutrientGoal

class BaseDietStructureNodeTest(BaseCodietTest):
    def setUp(self) -> None:
        super().setUp()

        self.diet_structure = DietStructure(OptimiserFixtures().monday_structure)

class TestAddressProperty(BaseDietStructureNodeTest):

    def test_address_property_returns_correct_address(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast", "Main"))
        self.assertEqual(node.address, ("Monday", "Breakfast", "Main"))

    def test_address_when_root_node(self):
        node = self.diet_structure.get_node(())
        self.assertEqual(node.address, ())

class TestIsRecipeNodeProperty(BaseDietStructureNodeTest):

    def test_is_recipe_node_when_leaf_node(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast", "Main"))
        self.assertTrue(node.is_recipe_node)

    def test_is_recipe_node_when_non_leaf_node(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast"))
        self.assertFalse(node.is_recipe_node)

class TestHasRecipeSolutionsProperty(BaseDietStructureNodeTest):
    
    def test_has_recipe_solutions_when_no_solutions(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast", "Main"))
        self.assertFalse(node.has_recipe_solutions)

    def test_has_recipe_solutions_when_has_solutions(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast", "Main"))

        recipe_quantity = self.recipe_factory.create_recipe_quantity_from_dto(
            {
                "recipe_name": "porridge", 
                "quantity": {
                    "unit_name": "gram", 
                    "value": 400
                }
            }
        )
        node.add_solution(
            solution=recipe_quantity,
            solution_set_id=1
        )

        self.assertTrue(node.has_recipe_solutions)

class TestAddConstraint(BaseDietStructureNodeTest):

    def test_can_add_constraint_to_leaf_node(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast", "Main"))
        self.assertEqual(len(node.constraints), 0)

        constraint = FlagConstraint("vegan", True)
        node.add_constraint(constraint)

        self.assertIn(constraint, node.constraints)

    def test_can_add_constraint_to_non_leaf_node(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast"))
        self.assertEqual(len(node.constraints), 0)

        constraint = FlagConstraint("vegan", True)
        node.add_constraint(constraint)

        self.assertIn(constraint, node.constraints)

class TestAddGoal(BaseDietStructureNodeTest):

    def test_can_add_goal_to_leaf_node(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast", "Main"))
        self.assertEqual(len(node.goals), 0)

        goal = MinimiseNutrientGoal("carbohydrate")
        node.add_goal(goal)

        self.assertIn(goal, node.goals)

    def test_can_add_goal_to_non_leaf_node(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast"))
        self.assertEqual(len(node.goals), 0)

        goal = MinimiseNutrientGoal("carbohydrate")
        node.add_goal(goal)

        self.assertIn(goal, node.goals)

class TestAddSolution(BaseDietStructureNodeTest):
    
    def test_cannot_add_solution_to_non_recipe_node(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast"))
        
        with self.assertRaises(ValueError):
            node.add_solution(self.recipe_fixtures.porridge_500g, 1)

    def test_can_add_solution_to_recipe_node(self):
        node = self.diet_structure.get_node(("Monday", "Breakfast", "Main"))
        self.assertEqual(len(node.solutions), 0)

        solution = self.recipe_fixtures.porridge_500g

        node.add_solution(solution, 1)

        self.assertEqual(node.solutions[1], solution)      
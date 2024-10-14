from codiet.tests import BaseCodietTest
from codiet.optimisation import DietStructure, DietStructureNode


class BaseDietStructureTest(BaseCodietTest):
    def setUp(self) -> None:
        super().setUp()
        self.monday_outline = {
            "Monday": {
                "Breakfast": {"Drink": {}, "Main": {}},
                "Lunch": {"Drink": {}, "Main": {}},
                "Dinner": {"Drink": {}, "Main": {}},
            }
        }


class TestConstructor(BaseDietStructureTest):

    def test_can_create_diet_structure(self):
        structure = DietStructure()

        self.assertIsInstance(structure, DietStructure)

    def test_can_create_with_structure(self):
        structure = DietStructure(self.monday_outline)

        self.assertIsInstance(structure, DietStructure)

class TestGetConstraints(BaseDietStructureTest):

    def test_gets_direct_and_parent_constraints_correctly(self):
        structure = DietStructure(self.monday_outline)

        vegan = self.constraint_factory.create_flag_constraint("vegan", True)
        vegetarian = self.constraint_factory.create_flag_constraint("vegetarian", True)
        
        structure.add_constraint(
            address=("Monday", "Breakfast"),
            constraint=vegan
        )
        structure.add_constraint(
            address=("Monday", "Breakfast", "Main"),
            constraint=vegetarian
        )

        constraints = structure.get_constraints(("Monday", "Breakfast", "Main"))

        self.assertEqual(len(constraints), 2)
        self.assertIn(vegan, constraints)
        self.assertIn(vegetarian, constraints)


class TestGetNode(BaseDietStructureTest):

    def test_can_get_node(self):
        structure = DietStructure(self.monday_outline)
        node = structure.get_node(("Monday", "Breakfast", "Main"))

        self.assertIsInstance(node, DietStructureNode)
        self.assertEqual(node.name, "Main")


class TestGetChildSolutions(BaseDietStructureTest):
    def test_get_child_solutions_from_root(self):
        structure = DietStructure(self.monday_outline)

        # Add solutions to the leaf nodes
        leaf_addresses = [
            ("Monday", "Breakfast", "Drink"),
            ("Monday", "Breakfast", "Main"),
            ("Monday", "Lunch", "Drink"),
            ("Monday", "Lunch", "Main"),
            ("Monday", "Dinner", "Drink"),
            ("Monday", "Dinner", "Main"),
        ]

        for address in leaf_addresses:
            node = structure.get_node(address)
            recipe = self.recipe_factory.create_new_recipe(name="_".join(address))
            node.add_solution(recipe, solution_set_id=1)

        # Get child solutions from the root
        all_solutions = structure.get_child_solutions()

        # Verify that all solutions are returned
        self.assertEqual(len(all_solutions), 6)
        recipe_names = [recipe.name for recipe in all_solutions]
        expected_names = [
            "Monday_Breakfast_Drink",
            "Monday_Breakfast_Main",
            "Monday_Lunch_Drink",
            "Monday_Lunch_Main",
            "Monday_Dinner_Drink",
            "Monday_Dinner_Main",
        ]
        for name in expected_names:
            self.assertIn(name, recipe_names)

    def test_get_child_solutions_from_subnode(self):
        structure = DietStructure(self.monday_outline)

        # Add solutions to the leaf nodes
        leaf_addresses = [
            ("Monday", "Breakfast", "Drink"),
            ("Monday", "Breakfast", "Main"),
            ("Monday", "Lunch", "Drink"),
            ("Monday", "Lunch", "Main"),
            ("Monday", "Dinner", "Drink"),
            ("Monday", "Dinner", "Main"),
        ]

        for address in leaf_addresses:
            node = structure.get_node(address)
            recipe = self.recipe_factory.create_new_recipe(name="_".join(address))
            node.add_solution(recipe, solution_set_id=1)

        # Get child solutions starting from "Monday -> Breakfast"
        breakfast_solutions = structure.get_child_solutions(
            starting_from_node=("Monday", "Breakfast")
        )

        # Verify that only breakfast solutions are returned
        self.assertEqual(len(breakfast_solutions), 2)
        recipe_names = [recipe.name for recipe in breakfast_solutions]
        expected_names = ["Monday_Breakfast_Drink", "Monday_Breakfast_Main"]
        for name in expected_names:
            self.assertIn(name, recipe_names)


class TestSolutionNodeAddresses(BaseDietStructureTest):

    def test_returns_correct_solution_node_addresses_from_root(self):
        structure = DietStructure(self.monday_outline)

        addresses = structure.solution_node_addresses()
        self.assertEqual(len(addresses), 6)
        expected_addresses = [
            ("Monday", "Breakfast", "Drink"),
            ("Monday", "Breakfast", "Main"),
            ("Monday", "Lunch", "Drink"),
            ("Monday", "Lunch", "Main"),
            ("Monday", "Dinner", "Drink"),
            ("Monday", "Dinner", "Main"),
        ]
        for address in expected_addresses:
            self.assertIn(address, addresses)

    def test_returns_correct_solution_node_addresses_from_subnode(self):
        structure = DietStructure(self.monday_outline)

        # Get solution node addresses starting from "Monday -> Lunch"
        addresses = structure.solution_node_addresses(
            starting_from_node=("Monday", "Lunch")
        )

        # Expected addresses
        expected_addresses = [("Monday", "Lunch", "Drink"), ("Monday", "Lunch", "Main")]

        self.assertEqual(len(addresses), 2)
        for address in expected_addresses:
            self.assertIn(address, addresses)


class TestSolutionNodes(BaseDietStructureTest):
    
    def test_returns_correct_solution_nodes_from_root(self):
        structure = DietStructure(self.monday_outline)

        nodes = structure.solution_nodes()
        self.assertEqual(len(nodes), 6)
        expected_nodes = [
            structure.get_node(("Monday", "Breakfast", "Drink")),
            structure.get_node(("Monday", "Breakfast", "Main")),
            structure.get_node(("Monday", "Lunch", "Drink")),
            structure.get_node(("Monday", "Lunch", "Main")),
            structure.get_node(("Monday", "Dinner", "Drink")),
            structure.get_node(("Monday", "Dinner", "Main"))
        ]
        for node in expected_nodes:
            self.assertIn(node, nodes)

    def test_returns_correct_solution_nodes_from_subnode(self):
        structure = DietStructure(self.monday_outline)

        # Get solution nodes starting from "Monday -> Dinner"
        nodes = structure.solution_nodes(starting_from_node=("Monday", "Dinner"))
        self.assertEqual(len(nodes), 2)
        expected_nodes = [
            structure.get_node(("Monday", "Dinner", "Drink")),
            structure.get_node(("Monday", "Dinner", "Main"))
        ]
        for node in expected_nodes:
            self.assertIn(node, nodes)


from codiet.tests import BaseCodietTest
from codiet.optimisation import DietStructure, DietStructureNode

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

class TestGetNode(BaseDietStructureTest):

    def test_can_get_node(self):
        structure = DietStructure(self.monday_outline)
        node = structure.get_node(("Monday", "Breakfast", "Main"))

        self.assertIsInstance(node, DietStructureNode)
        self.assertEqual(node.name, "Main")

class TestRecipeAddresses(BaseDietStructureTest):
    
    def test_returns_recipe_node_addresses(self):
        structure = DietStructure(self.monday_outline)

        self.assertTrue(len(structure.recipe_node_addresses) == 6)

        self.assertTrue(("Monday", "Breakfast", "Drink") in structure.recipe_node_addresses)
        self.assertTrue(("Monday", "Breakfast", "Main") in structure.recipe_node_addresses)
        self.assertTrue(("Monday", "Lunch", "Drink") in structure.recipe_node_addresses)
        self.assertTrue(("Monday", "Lunch", "Main") in structure.recipe_node_addresses)
        self.assertTrue(("Monday", "Dinner", "Drink") in structure.recipe_node_addresses)
        self.assertTrue(("Monday", "Dinner", "Main") in structure.recipe_node_addresses)

class TestGetRecipeNode(BaseDietStructureTest):

    def test_can_get_recipe_node(self):
        structure = DietStructure(self.monday_outline)
        
        self.assertEqual(len(structure.recipe_nodes), 6)
        for node in structure.recipe_nodes:
            self.assertTrue(node.is_recipe_node)

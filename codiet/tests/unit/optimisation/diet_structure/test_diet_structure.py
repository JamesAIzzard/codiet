from codiet.tests import BaseCodietTest

from codiet.optimisation import DietStructure

class BaseDietStructureTest(BaseCodietTest):
    pass

class TestConstructor(BaseDietStructureTest):
    
    def test_can_create_diet_structure(self):
        structure = DietStructure()

        self.assertIsInstance(structure, DietStructure)

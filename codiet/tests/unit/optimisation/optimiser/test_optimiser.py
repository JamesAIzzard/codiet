from codiet.tests import BaseCodietTest
from codiet.optimisation import Optimiser

class BaseOptimiserTest(BaseCodietTest):
    pass

class TestConstructor(BaseOptimiserTest):
    
    def test_can_create_optimiser(self):
        optimiser = Optimiser()

        self.assertIsInstance(optimiser, Optimiser)
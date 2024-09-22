from codiet.tests import BaseCodietTest
from codiet.optimisation.constraints import FlagConstraint

class BaseFlagConstraintTest(BaseCodietTest):
    pass

class TestConstructor(BaseFlagConstraintTest):
    
    def test_can_create_instance(self):
        constraint = FlagConstraint("vegan", True)

        self.assertIsInstance(constraint, FlagConstraint)
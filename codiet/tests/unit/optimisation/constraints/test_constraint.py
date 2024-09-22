from codiet.tests import BaseCodietTest
from codiet.optimisation import Constraint

class BaseConstraintTest(BaseCodietTest):
    pass

class TestConstructor(BaseConstraintTest):
    
    def test_can_create_instance(self):
        constraint = Constraint()

        self.assertIsInstance(constraint, Constraint)
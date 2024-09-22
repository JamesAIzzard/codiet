from codiet.tests import BaseCodietTest

from codiet.optimisation import Goal

class BaseGoalTest(BaseCodietTest):
    pass

class TestConstructor(BaseGoalTest):
    
    def test_can_create_instance(self):
        goal = Goal()

        self.assertIsInstance(goal, Goal)
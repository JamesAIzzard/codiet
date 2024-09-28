from codiet.tests import BaseCodietTest
from codiet.model.flags.flag import Flag

class BaseFlagTest(BaseCodietTest):
    pass

class TestConstructor(BaseFlagTest):
    def test_minimal_arguments(self):
        flag = Flag("test_flag")
        self.assertIsInstance(flag, Flag)

class TestEquality(BaseFlagTest):
    def test_true_equality(self):
        flag1 = Flag("test_flag")
        flag2 = Flag("test_flag")
        self.assertEqual(flag1, flag2)

    def test_false_equality(self):
        flag1 = Flag("test_flag1")
        flag2 = Flag("test_flag2")
        self.assertNotEqual(flag1, flag2)
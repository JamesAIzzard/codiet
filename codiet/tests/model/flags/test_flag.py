"""Unit tests for the flag class."""

from codiet.tests.model import BaseModelTest
from codiet.model.flags.flag import Flag

class BaseFlagTest(BaseModelTest):
    """Base class for testing flags."""
    pass

class TestConstructor(BaseFlagTest):
    def test_minimal_arguments(self):
        """Check that the flag can be constructed with minimal arguments."""
        flag = Flag("test_flag")
        self.assertIsInstance(flag, Flag)

class TestEquality(BaseFlagTest):
    def test_true_equality(self):
        """Check that two flags with the same name are considered equal."""
        flag1 = Flag("test_flag")
        flag2 = Flag("test_flag")
        self.assertEqual(flag1, flag2)

    def test_false_equality(self):
        """Check that two flags with different names are not considered equal."""
        flag1 = Flag("test_flag1")
        flag2 = Flag("test_flag2")
        self.assertNotEqual(flag1, flag2)
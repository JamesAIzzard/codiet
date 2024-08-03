import unittest
from codiet.models.flags.flag import Flag

class TestFlag(unittest.TestCase):
    def test_init(self):
        """Test the initialisation of Flag."""
        flag = Flag("test_flag")
        self.assertEqual(flag.flag_name, "test_flag")
        self.assertFalse(flag.flag_value)

        flag_with_value = Flag("value_flag", True)
        self.assertEqual(flag_with_value.flag_name, "value_flag")
        self.assertTrue(flag_with_value.flag_value)

    def test_value_setter(self):
        """Test the setter for flag_value."""
        flag = Flag("test_flag")
        self.assertFalse(flag.flag_value)

        flag.flag_value = True
        self.assertTrue(flag.flag_value)

        flag.flag_value = False
        self.assertFalse(flag.flag_value)

    def test_equality(self):
        """Test the equality of two flags."""
        flag1 = Flag("test_flag")
        flag2 = Flag("test_flag")
        self.assertEqual(flag1, flag2)

        flag3 = Flag("different_flag")
        self.assertNotEqual(flag1, flag3)
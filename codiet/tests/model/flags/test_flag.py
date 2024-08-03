import unittest
from codiet.models.flags.flag import Flag

class TestFlag(unittest.TestCase):
    def test_flag_initialisation(self):
        flag = Flag("test_flag")
        self.assertEqual(flag.flag_name, "test_flag")
        self.assertFalse(flag.flag_value)

        flag_with_value = Flag("value_flag", True)
        self.assertEqual(flag_with_value.flag_name, "value_flag")
        self.assertTrue(flag_with_value.flag_value)

    def test_flag_value_setter(self):
        """Test the setter for flag_value."""
        flag = Flag("test_flag")
        self.assertFalse(flag.flag_value)

        flag.flag_value = True
        self.assertTrue(flag.flag_value)

        flag.flag_value = False
        self.assertFalse(flag.flag_value)
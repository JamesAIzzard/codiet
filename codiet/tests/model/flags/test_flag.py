import unittest
from codiet.model.flags.flag import Flag

class TestFlag(unittest.TestCase):
    def test_init(self):
        """Test the initialisation of Flag."""
        flag = Flag(flag_name="test_flag")
        self.assertEqual(flag.flag_name, "test_flag")

        flag_with_value = Flag(flag_name="value_flag")
        self.assertEqual(flag_with_value.flag_name, "value_flag")



    def test_equality(self):
        """Test the equality of two flags."""
        flag1 = Flag("test_flag")
        flag2 = Flag("test_flag")
        self.assertEqual(flag1, flag2)

        flag3 = Flag("different_flag")
        self.assertNotEqual(flag1, flag3)
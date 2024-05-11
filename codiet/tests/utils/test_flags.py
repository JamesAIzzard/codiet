import unittest

from codiet.utils.flags import get_missing_flags

class TestGetMissingFlags(unittest.TestCase):
    """Test the get_missing_flags function."""

    def test_finds_no_missing_flags(self):
        """Test that the function returns an empty list when no flags are missing."""
        flag_list = ['flag1', 'flag2', 'flag3']
        global_flag_list = ['flag1', 'flag2', 'flag3']

        result = get_missing_flags(flag_list, global_flag_list)

        self.assertEqual(result, [])

    def test_finds_missing_flags_correctly(self):
        """Test that the function returns the correct list of missing flags."""
        flag_list = ['flag1', 'flag2', 'flag3']
        global_flag_list = ['flag1', 'flag3', 'flag4']
        expected_result = ['flag4']

        result = get_missing_flags(flag_list, global_flag_list)

        self.assertEqual(result, expected_result)

    def test_finds_all_flags_missing(self):
        """Test that all missing flags are found when the flag list is empty."""
        flag_list = []
        global_flag_list = ['flag1', 'flag2', 'flag3']

        result = get_missing_flags(flag_list, global_flag_list)

        self.assertEqual(result, global_flag_list)

if __name__ == '__main__':
    unittest.main()
import unittest

from codiet.tests.unit.utils.unique_collection import Simple
from codiet.utils.unique_collection import ImmutableUniqueCollection

class TestImmutableUniqueCollection(unittest.TestCase):
    def setUp(self):
        self.sample_list = [1, 2, 3, 4, 5]
        self.sample_tuple = (1, 2, 3, 4, 5)
        self.sample_set = {1, 2, 3, 4, 5}

        self.simple_1 = Simple(1, "one")
        self.simple_2 = Simple(2, "two")
        self.simple_3 = Simple(3, "three")
        self.simples = [self.simple_1, self.simple_2, self.simple_3]

    def test_init(self):
        """Checks we can initialise the class with a variety of collection types."""

        # Check with no args
        self.empty_list = ImmutableUniqueCollection()
        self.assertEqual(len(self.empty_list), 0)

        # Check with a list
        self.uc = ImmutableUniqueCollection(self.sample_list)
        self.assertEqual(len(self.uc), 5)
        self.assertEqual(list(self.uc), self.sample_list)

        # Check with a tuple
        self.list_tuple = ImmutableUniqueCollection(self.sample_tuple)
        self.assertEqual(len(self.list_tuple), 5)
        self.assertEqual(list(self.list_tuple), self.sample_list)

        # Check with a set
        self.list_set = ImmutableUniqueCollection(self.sample_set)
        self.assertEqual(len(self.list_set), 5)
        self.assertEqual(list(self.list_set), self.sample_list)

    def test_value_error_if_non_unique_init(self):
        """Check we get an error if we try to initialise with non-unique items."""
        with self.assertRaises(ValueError):
            ImmutableUniqueCollection([1, 1, 2, 3, 4, 5])

    def test_in(self):
        """Check the in and not in operators work as expected."""
        self.uc = ImmutableUniqueCollection(self.sample_list)

        # Check that in works
        self.assertTrue(1 in self.uc)
        self.assertFalse(6 in self.uc)

        # Check that not in works
        self.assertFalse(1 not in self.uc)
        self.assertTrue(6 not in self.uc)
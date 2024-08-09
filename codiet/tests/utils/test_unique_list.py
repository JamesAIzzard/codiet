import unittest

from codiet.utils.unique_list import UniqueList

# Create a simple which is equal on one property and not equal on another
class Simple:
    def __init__(self, id, some_value):
        self.id = id
        self.some_value = some_value

    def __eq__(self, other):
        return self.id == other.a

    def __hash__(self):
        return hash(self.id)

class TestUniqueList(unittest.TestCase):
    def setUp(self):
        self.sample_list = [1, 2, 3, 4, 5]
        self.sample_tuple = (1, 2, 3, 4, 5)
        self.sample_set = {1, 2, 3, 4, 5}

    def test_init(self):
        self.empty_list = UniqueList()
        self.assertEqual(len(self.empty_list), 0)

        self.ul = UniqueList(self.sample_list)
        self.assertEqual(len(self.ul), 5)
        self.assertEqual(list(self.ul), self.sample_list)

        self.list_tuple = UniqueList(self.sample_tuple)
        self.assertEqual(len(self.list_tuple), 5)
        self.assertEqual(list(self.list_tuple), self.sample_list)

        self.list_set = UniqueList(self.sample_set)
        self.assertEqual(len(self.list_set), 5)
        self.assertEqual(list(self.list_set), self.sample_list)

    def test_value_error_if_non_unique_init(self):
        with self.assertRaises(ValueError):
            UniqueList([1, 1, 2, 3, 4, 5])

    def test_add(self):
        self.ul = UniqueList()

        # Check we can add a single item
        self.ul.add(1)
        self.assertEqual(len(self.ul), 1)
        self.assertEqual(list(self.ul), [1])

        # Check we can add another single item
        self.ul.add(2)
        self.assertEqual(len(self.ul), 2)
        self.assertEqual(list(self.ul), [1, 2])

        # Check we can add a list of items
        self.ul.add([3, 4, 5])
        self.assertEqual(len(self.ul), 5)
        self.assertEqual(list(self.ul), [1, 2, 3, 4, 5])

        # Check we can add a tuple of items
        self.ul.add((6, 7, 8))
        self.assertEqual(len(self.ul), 8)

        # Check we can add a set of items
        self.ul.add({9, 10, 11})
        self.assertEqual(len(self.ul), 11)

    def test_value_error_if_non_unique_add(self):
        self.ul = UniqueList()

        self.ul.add(1)
        self.ul.add(2)
        self.ul.add(3)

        with self.assertRaises(ValueError):
            self.ul.add(1)

        # Check the same if we add multiples
        with self.assertRaises(ValueError):
            self.ul.add([1, 2, 3])

    def test_remove(self):
        self.ul = UniqueList(self.sample_list)

        # Check we can remove a single item
        self.ul.remove(1)
        self.assertEqual(len(self.ul), 4)
        self.assertEqual(list(self.ul), [2, 3, 4, 5])

        # Check we can remove a list of items
        self.ul.remove([2, 3, 4])
        self.assertEqual(len(self.ul), 1)
        self.assertEqual(list(self.ul), [5])

        # Check we can remove a tuple of items
        self.ul.remove((5,))
        self.assertEqual(len(self.ul), 0)

        # Check we can remove a set of items
        self.ul = UniqueList(self.sample_list)
        self.ul.remove({1, 2, 3})
        self.assertEqual(len(self.ul), 2)
        self.assertEqual(list(self.ul), [4, 5])

    def test_update(self):
        self.ul = UniqueList[Simple]()

        # Create a list of simples
        simple_1 = Simple(1, "one")
        simple_2 = Simple(2, "two")
        simple_3 = Simple(3, "three")

        # Add them all
        self.ul.add([simple_1, simple_2, simple_3])

        # Update the first one
        simple_1.some_value = "new value"
        self.ul.update(simple_1)

        # Check the list is updated
        self.assertEqual(len(self.ul), 3)

        # Update two and three
        simple_2.some_value = "new value"
        simple_3.some_value = "new value"
        self.ul.update([simple_2, simple_3])

        # Check all the values are now correct
        self.assertEqual(len(self.ul), 3)
        self.assertEqual(self.ul[0].some_value, "new value")
        self.assertEqual(self.ul[1].some_value, "new value")
        self.assertEqual(self.ul[2].some_value, "new value")

        # Check we get an error if we try to update a non-existent item
        with self.assertRaises(ValueError):
            self.ul.update(Simple(4, "four"))

    def test_freeze(self):
        self.ul = UniqueList(self.sample_list)
        self.assertEqual(self.ul.freeze(), tuple(self.sample_list))

        self.ul = UniqueList()
        self.assertEqual(self.ul.freeze(), tuple())

    
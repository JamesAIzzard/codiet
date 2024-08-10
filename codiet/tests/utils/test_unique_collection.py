import unittest

from codiet.utils.unique_collection import UniqueCollection

# Create a simple which is equal on one property and not equal on another
class Simple:
    def __init__(self, id, some_value):
        self.id = id
        self.some_value = some_value

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class TestUniqueCollection(unittest.TestCase):
    def setUp(self):
        self.sample_list = [1, 2, 3, 4, 5]
        self.sample_tuple = (1, 2, 3, 4, 5)
        self.sample_set = {1, 2, 3, 4, 5}

        self.simple_1 = Simple(1, "one")
        self.simple_2 = Simple(2, "two")
        self.simple_3 = Simple(3, "three")
        self.simples = [self.simple_1, self.simple_2, self.simple_3]

    def test_init(self):
        self.empty_list = UniqueCollection()
        self.assertEqual(len(self.empty_list), 0)

        self.uc = UniqueCollection(self.sample_list)
        self.assertEqual(len(self.uc), 5)
        self.assertEqual(list(self.uc), self.sample_list)

        self.list_tuple = UniqueCollection(self.sample_tuple)
        self.assertEqual(len(self.list_tuple), 5)
        self.assertEqual(list(self.list_tuple), self.sample_list)

        self.list_set = UniqueCollection(self.sample_set)
        self.assertEqual(len(self.list_set), 5)
        self.assertEqual(list(self.list_set), self.sample_list)

    def test_value_error_if_non_unique_init(self):
        with self.assertRaises(ValueError):
            UniqueCollection([1, 1, 2, 3, 4, 5])

    def test_in(self):
        self.uc = UniqueCollection(self.sample_list)

        # Check that in works
        self.assertTrue(1 in self.uc)
        self.assertFalse(6 in self.uc)

        # Check that not in works
        self.assertFalse(1 not in self.uc)
        self.assertTrue(6 not in self.uc)

    def test_add(self):
        self.uc = UniqueCollection()

        # Check we can add a single item
        self.uc.add(1)
        self.assertEqual(len(self.uc), 1)
        self.assertEqual(list(self.uc), [1])

        # Check we can add another single item
        self.uc.add(2)
        self.assertEqual(len(self.uc), 2)
        self.assertEqual(list(self.uc), [1, 2])

        # Check we can add a list of items
        self.uc.add([3, 4, 5])
        self.assertEqual(len(self.uc), 5)
        self.assertEqual(list(self.uc), [1, 2, 3, 4, 5])

        # Check we can add a tuple of items
        self.uc.add((6, 7, 8))
        self.assertEqual(len(self.uc), 8)

        # Check we can add a set of items
        self.uc.add({9, 10, 11})
        self.assertEqual(len(self.uc), 11)

    def test_value_error_if_non_unique_add(self):
        self.uc = UniqueCollection()

        self.uc.add(1)
        self.uc.add(2)
        self.uc.add(3)

        with self.assertRaises(ValueError):
            self.uc.add(1)

        # Check the same if we add multiples
        with self.assertRaises(ValueError):
            self.uc.add([1, 2, 3])

    def test_remove(self):
        self.uc = UniqueCollection(self.sample_list)

        # Check we can remove a single item
        self.uc.remove(1)
        self.assertEqual(len(self.uc), 4)
        self.assertEqual(list(self.uc), [2, 3, 4, 5])

        # Check we can remove a list of items
        self.uc.remove([2, 3, 4])
        self.assertEqual(len(self.uc), 1)
        self.assertEqual(list(self.uc), [5])

        # Check we can remove a tuple of items
        self.uc.remove((5,))
        self.assertEqual(len(self.uc), 0)

        # Check we can remove a set of items
        self.uc = UniqueCollection(self.sample_list)
        self.uc.remove({1, 2, 3})
        self.assertEqual(len(self.uc), 2)
        self.assertEqual(list(self.uc), [4, 5])

    def test_update(self):
        self.uc = UniqueCollection[Simple]()

        # Create a list of simples
        simple_1 = Simple(1, "one")
        simple_2 = Simple(2, "two")
        simple_3 = Simple(3, "three")

        # Add them all
        self.uc.add([simple_1, simple_2, simple_3])

        # Update the first one
        updated_simple_1 = Simple(1, "new value")
        self.uc.update(updated_simple_1)

        # Check the list is updated
        for item in self.uc:
            if item.id == 1:
                self.assertEqual(item.some_value, "new value")

        # Update two and three
        simple_2.some_value = "new value"
        simple_3.some_value = "new value"
        self.uc.update([simple_2, simple_3])

        # Check all the values are now correct
        self.assertEqual(len(self.uc), 3)
        self.assertEqual(self.uc[0].some_value, "new value")
        self.assertEqual(self.uc[1].some_value, "new value")
        self.assertEqual(self.uc[2].some_value, "new value")

        # Check we get an error if we try to update a non-existent item
        with self.assertRaises(ValueError):
            self.uc.update(Simple(4, "four"))

    def test_updates_even_when_object_is_equal(self):
        uc = UniqueCollection[Simple]()

        # Add the simples to the instance
        uc.add(self.simples)

        # Grab the memory address of the first simple
        original_id = id(uc[0])

        # Update the first one with an object that is equal but not the same
        updated_simple_1 = Simple(1, "new value")
        uc.update(updated_simple_1)

        # Check the list is updated
        for item in uc:
            if item.id == 1:
                self.assertEqual(item.some_value, "new value")
                # Check the memory address is different
                self.assertNotEqual(id(item), original_id)

    def test_can_convert_to_tuple(self):
        self.uc = UniqueCollection(self.sample_list)
        self.assertEqual(tuple(self.uc), self.sample_tuple)
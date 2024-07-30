import unittest

from codiet.utils.map.map import Map

class TestMap(unittest.TestCase):


    def test_constructor_default(self):
        """
        Test the default constructor behavior of Map.

        This test verifies that:
        1. An empty map is created successfully.
        2. The one_to_one flag is set to True by default.
        3. The map contains no keys or values initially.
        """
        bm = Map()
        self.assertTrue(bm.one_to_one)
        self.assertEqual(len(bm.keys), 0)
        self.assertEqual(len(bm.values), 0)

    def test_constructor_with_lists_default_one_to_one(self):
        """
        Test the constructor with lists in default one-to-one mode.

        This test verifies that:
        1. The one_to_one flag is True by default.
        2. The mappings are created correctly in both directions.
        3. Each key maps to exactly one value and vice versa.
        4. The number of keys and values match the input lists.
        """
        from_list = [1, 2, 3]
        to_list = ['one', 'two', 'three']
        bm = Map(from_list=from_list, to_list=to_list)
        
        self.assertTrue(bm.one_to_one)
        self.assertEqual(bm.get_values(1), ['one'])
        self.assertEqual(bm.get_keys('one'), [1])
        self.assertEqual(len(bm.keys), 3)
        self.assertEqual(len(bm.values), 3)

    def test_constructor_with_lists_many_to_many(self):
        """
        Test the constructor with lists in many-to-many mode.

        This test verifies that:
        1. The one_to_one flag is set to False when specified.
        2. The mappings are created correctly in both directions.
        3. Multiple values can be associated with a single key and vice versa.
        4. The number of keys and values are correct for duplicate mappings.
        """
        from_list = [1, 2, 3, 1]
        to_list = ['one', 'two', 'three', 'uno']
        bm = Map(from_list=from_list, to_list=to_list, one_to_one=False)
        
        self.assertFalse(bm.one_to_one)
        self.assertEqual(bm.get_values(1), ['one', 'uno'])
        self.assertEqual(bm.get_keys('one'), [1])
        self.assertEqual(bm.get_keys('uno'), [1])
        self.assertEqual(len(bm.keys), 3)
        self.assertEqual(len(bm.values), 4)

    def test_constructor_with_unequal_lists(self):
        """
        Test the constructor's error handling with unequal lists.

        This test verifies that:
        1. A ValueError is raised when from_list and to_list have different lengths.
        """
        from_list = [1, 2, 3]
        to_list = ['one', 'two']
        
        with self.assertRaises(ValueError):
            Map(from_list=from_list, to_list=to_list)

    def test_constructor_with_duplicate_values_one_to_one(self):
        """
        Test the constructor's error handling with duplicate values in one-to-one mode.

        This test verifies that:
        1. A ValueError is raised when attempting to create a one-to-one map with duplicate keys or values.
        """
        from_list = [1, 2, 3, 1]
        to_list = ['one', 'two', 'three', 'uno']
        
        with self.assertRaises(ValueError):
            Map(from_list=from_list, to_list=to_list)

    def test_add_mapping_one_to_one(self):
        """
        Test adding mappings in one-to-one mode.

        This test verifies that:
        1. Adding a new mapping works correctly.
        2. The mapping is accessible in both directions.
        3. Adding a duplicate key or value raises a ValueError.
        """
        bm = Map()
        bm.add_mapping(1, "one")
        
        self.assertEqual(bm.get_values(1), ["one"])
        self.assertEqual(bm.get_keys("one"), [1])
        
        with self.assertRaises(ValueError):
            bm.add_mapping(1, "uno")
        
        with self.assertRaises(ValueError):
            bm.add_mapping(2, "one")

    def test_add_mapping_many_to_many(self):
        """
        Test adding mappings in many-to-many mode.

        This test verifies that:
        1. Multiple mappings can be added for the same key or value.
        2. The mappings are correctly stored and accessible in both directions.
        """
        bm = Map(one_to_one=False)
        bm.add_mapping(1, "one")
        bm.add_mapping(1, "uno")
        bm.add_mapping(2, "two")
        
        self.assertEqual(bm.get_values(1), ["one", "uno"])
        self.assertEqual(bm.get_keys("one"), [1])
        self.assertEqual(bm.get_values(2), ["two"])

    def test_remove_mapping(self):
        """
        Test removing a specific mapping.

        This test verifies that:
        1. A specific key-value mapping can be removed.
        2. The removal is reflected in both directions.
        3. Other mappings for the same key remain intact.
        """
        bm = Map(one_to_one=False)
        bm.add_mapping(1, "one")
        bm.add_mapping(1, "uno")
        bm.remove_mapping(1, "one")
        
        self.assertEqual(bm.get_values(1), ["uno"])
        self.assertEqual(bm.get_keys("one"), [])

    def test_remove_key(self):
        """
        Test removing all mappings for a given key.

        This test verifies that:
        1. All mappings associated with a key are removed.
        2. The removal is reflected in both directions.
        3. Accessing the removed key or its associated values returns None.
        """
        bm = Map(one_to_one=False)
        bm.add_mapping(1, "one")
        bm.add_mapping(1, "uno")
        bm.remove_key(1)
        
        self.assertEqual([], bm.get_values(1))
        self.assertEqual([], bm.get_keys("one"))
        self.assertEqual([], bm.get_keys("uno"))

    def test_remove_value(self):
        """
        Test removing all mappings for a given value.

        This test verifies that:
        1. All mappings associated with a value are removed.
        2. The removal is reflected in both directions.
        3. Accessing the removed value or its associated keys returns None.
        """
        bm = Map(one_to_one=False)
        bm.add_mapping(1, "one")
        bm.add_mapping(2, "one")
        bm.remove_value("one")
        
        self.assertEqual([], bm.get_values(1))
        self.assertEqual([], bm.get_values(2))
        self.assertEqual([], bm.get_keys("one"))

    def test_keys_and_values_properties(self):
        """
        Test the keys and values properties.

        This test verifies that:
        1. The keys property returns all keys in the map.
        2. The values property returns all values in the map.
        3. The returned keys and values are correct for the given mappings.
        """
        bm = Map()
        bm.add_mapping(1, "one")
        bm.add_mapping(2, "two")
        
        self.assertEqual(set(bm.keys), {1, 2})
        self.assertEqual(set(bm.values), {"one", "two"})

    def test_get_value(self):
        """
        Test the get_value method.

        This test verifies that:
        1. get_value returns the correct single value for a given key.
        2. get_value raises a ValueError when a key is not found.
        3. get_value raises a ValueError when multiple values exist for a key in many-to-many mode.
        """
        bm = Map()
        bm.add_mapping(1, "one")
        bm.add_mapping(2, "two")
        
        self.assertEqual(bm.get_value(1), "one")
        self.assertEqual(bm.get_value(2), "two")
        self.assertRaises(ValueError, bm.get_value, 3)
        
        # Test many-to-many scenario
        bm_many = Map(one_to_one=False)
        bm_many.add_mapping(1, "one")
        bm_many.add_mapping(1, "uno")
        
        with self.assertRaises(ValueError):
            bm_many.get_value(1)

    def test_get_key(self):
        """
        Test the get_key method.

        This test verifies that:
        1. get_key returns the correct single key for a given value.
        2. get_key raises a ValueError when a value is not found.
        3. get_key raises a ValueError when multiple keys exist for a value in many-to-many mode.
        """
        bm = Map()
        bm.add_mapping(1, "one")
        bm.add_mapping(2, "two")
        
        self.assertEqual(bm.get_key("one"), 1)
        self.assertEqual(bm.get_key("two"), 2)
        self.assertRaises(ValueError, bm.get_key, "three")
        
        # Test many-to-many scenario
        bm_many = Map(one_to_one=False)
        bm_many.add_mapping(1, "one")
        bm_many.add_mapping(2, "one")
        
        with self.assertRaises(ValueError):
            bm_many.get_key("one")

    def test_get_value_and_get_key_with_many_to_many(self):
        """
        Test get_value and get_key methods in many-to-many mode.

        This test verifies that:
        1. Both methods raise ValueError when multiple mappings exist.
        2. Both methods raise ValueError when the key or value is not found.
        3. The methods work correctly for unique mappings in many-to-many mode.
        """
        bm = Map(one_to_one=False)
        bm.add_mapping("a", 1)
        bm.add_mapping("b", 2)
        bm.add_mapping("c", 2)
        bm.add_mapping("a", 3)
        
        with self.assertRaises(ValueError):
            bm.get_value("a")
        
        with self.assertRaises(ValueError):
            bm.get_key(2)
        
        self.assertEqual(bm.get_value("b"), 2)
        self.assertEqual(bm.get_key(1), "a")
        
        self.assertRaises(ValueError, bm.get_value, "d")
        self.assertRaises(ValueError, bm.get_key, 4)      
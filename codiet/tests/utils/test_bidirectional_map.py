import unittest

from codiet.utils.bidirectional_map import BidirectionalMap

class TestBidirectionalMap(unittest.TestCase):

    def setUp(self):
        bm = BidirectionalMap()
        self.assertEqual(len(bm.keys), 0)
        self.assertEqual(len(bm.values), 0)

    def test_add_mapping_many_to_many(self):
        bm = BidirectionalMap()
        bm.add_mapping(1, "one")
        bm.add_mapping(1, "uno")
        bm.add_mapping(2, "two")
        
        self.assertEqual(bm.get_values(1), ["one", "uno"])
        self.assertEqual(bm.get_keys("one"), [1])
        self.assertEqual(bm.get_values(2), ["two"])

    def test_add_mapping_one_to_one(self):
        bm = BidirectionalMap(one_to_one=True)
        bm.add_mapping(1, "one")
        
        with self.assertRaises(ValueError):
            bm.add_mapping(1, "uno")
        
        with self.assertRaises(ValueError):
            bm.add_mapping(2, "one")

    def test_remove_mapping(self):
        bm = BidirectionalMap()
        bm.add_mapping(1, "one")
        bm.add_mapping(1, "uno")
        bm.remove_mapping(1, "one")
        
        self.assertEqual(bm.get_values(1), ["uno"])
        self.assertIsNone(bm.get_keys("one"))

    def test_remove_key(self):
        bm = BidirectionalMap()
        bm.add_mapping(1, "one")
        bm.add_mapping(1, "uno")
        bm.remove_key(1)
        
        self.assertIsNone(bm.get_values(1))
        self.assertIsNone(bm.get_keys("one"))
        self.assertIsNone(bm.get_keys("uno"))

    def test_remove_value(self):
        bm = BidirectionalMap()
        bm.add_mapping(1, "one")
        bm.add_mapping(2, "one")
        bm.remove_value("one")
        
        self.assertIsNone(bm.get_values(1))
        self.assertIsNone(bm.get_values(2))
        self.assertIsNone(bm.get_keys("one"))

    def test_keys_and_values_properties(self):
        bm = BidirectionalMap()
        bm.add_mapping(1, "one")
        bm.add_mapping(2, "two")
        
        self.assertEqual(set(bm.keys), {1, 2})
        self.assertEqual(set(bm.values), {"one", "two"})
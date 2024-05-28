import unittest

from codiet.utils.tags import flatten_tree

class TestFlattenTree(unittest.TestCase):
    """Test the flatten_tree function."""

    def test_flattens_empty_tree(self):
        """Test that the function returns an empty list when the tree is empty."""
        tree = {}

        result = flatten_tree(tree)

        self.assertEqual(result, [])

    def test_flattens_single_level_tree(self):
        """Test that the function correctly flattens a single-level tree."""
        tree = {'key1': {}, 'key2': {}}

        result = flatten_tree(tree)

        self.assertEqual(result, ['key1', 'key2'])

    def test_flattens_nested_tree(self):
        """Test that the function correctly flattens a nested tree."""
        tree = {
            'key1': {
                'key2': 'value2',
                'key3': {
                    'key4': 'value4'
                }
            },
            'key5': 'value5'
        }

        result = flatten_tree(tree)

        self.assertEqual(result, ['key1', 'key1/key2', 'key1/key3', 'key1/key3/key4', 'key5'])
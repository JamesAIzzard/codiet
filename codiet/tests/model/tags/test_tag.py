from unittest import TestCase

from codiet.model.tags.tag import Tag

class TestTag(TestCase):

    def setUp(self):
        pass

    def test_init_without_id(self):
        """Check we can initialise the tag without an ID."""
        tag = Tag(tag_name="Test")
        # Check its the right type
        self.assertIsInstance(tag, Tag)
        # Check the tag name is correct
        self.assertEqual(tag.tag_name, "Test")
        # Check the ID is None
        self.assertIsNone(tag.id)
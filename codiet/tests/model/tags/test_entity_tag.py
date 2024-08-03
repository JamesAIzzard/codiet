from unittest import TestCase

from codiet.models.tags.entity_tag import EntityTag

class TestEntityTag(TestCase):

    def setUp(self):
        pass

    def test_init_without_ids(self):
        """Check we can initialise the tag without an ID."""
        tag = EntityTag(tag_name="Test")
        # Check its the right type
        self.assertIsInstance(tag, EntityTag)
        # Check the tag name is correct
        self.assertEqual(tag.tag_name, "Test")
        # Check the ID is None
        self.assertIsNone(tag.id)

    def test_init_with_id(self):
        """Check we can initialise the tag with an ID."""
        tag = EntityTag(tag_name="Test", id=1)
        # Check its the right type
        self.assertIsInstance(tag, EntityTag)
        # Check the tag name is correct
        self.assertEqual(tag.tag_name, "Test")
        # Check the ID is correct
        self.assertEqual(tag.id, 1)

    def test_init_with_ref_entity_id(self):
        """Check we can initialise the tag with a reference entity ID."""
        tag = EntityTag(tag_name="Test", ref_entity_id=1)
        # Check its the right type
        self.assertIsInstance(tag, EntityTag)
        # Check the tag name is correct
        self.assertEqual(tag.tag_name, "Test")
        # Check the reference entity ID is correct
        self.assertEqual(tag.ref_entity_id, 1)
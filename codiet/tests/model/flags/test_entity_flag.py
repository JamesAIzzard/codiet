from unittest import TestCase

from codiet.models.flags.entity_flag import EntityFlag
from codiet.db.stored_ref_entity import StoredRefEntity
from codiet.db.stored_entity import StoredEntity

class TestEntityFlag(TestCase):
    def test_entity_flag_initialisation(self):
        entity_flag = EntityFlag("test_entity_flag")
        self.assertEqual(entity_flag.flag_name, "test_entity_flag")
        self.assertFalse(entity_flag.flag_value)

        entity_flag_with_value = EntityFlag("value_entity_flag", True)
        self.assertEqual(entity_flag_with_value.flag_name, "value_entity_flag")
        self.assertTrue(entity_flag_with_value.flag_value)

    def test_entity_flag_value_setter(self):
        """Test the setter for flag_value in EntityFlag."""
        entity_flag = EntityFlag("test_entity_flag")
        self.assertFalse(entity_flag.flag_value)

        entity_flag.flag_value = True
        self.assertTrue(entity_flag.flag_value)

        entity_flag.flag_value = False
        self.assertFalse(entity_flag.flag_value)

    def test_entity_flag_inheritance(self):
        """Test that EntityFlag inherits from both Flag and StoredRefEntity."""
        entity_flag = EntityFlag("test_entity_flag")
        self.assertIsInstance(entity_flag, EntityFlag)
        self.assertIsInstance(entity_flag, StoredRefEntity)
        self.assertIsInstance(entity_flag, StoredEntity)

    def test_entity_flag_stored_ref_entity_properties(self):
        """Test StoredRefEntity properties in EntityFlag."""
        entity_flag = EntityFlag("test_flag", primary_entity_id=1, ref_entity_id=2)
        self.assertEqual(entity_flag.primary_entity_id, 1)
        self.assertEqual(entity_flag.ref_entity_id, 2)

        entity_flag.primary_entity_id = 3
        self.assertEqual(entity_flag.primary_entity_id, 3)

        entity_flag.ref_entity_id = 4
        self.assertEqual(entity_flag.ref_entity_id, 4)

    def test_entity_flag_stored_entity_properties(self):
        """Test StoredEntity properties in EntityFlag."""
        entity_flag = EntityFlag("test_flag", id=5)
        self.assertEqual(entity_flag.id, 5)
        self.assertTrue(entity_flag.is_persisted)

        entity_flag.id = None
        self.assertIsNone(entity_flag.id)
        self.assertFalse(entity_flag.is_persisted)

        with self.assertRaises(ValueError):
            entity_flag.id = "not an integer" # type: ignore # This is intentional to test the error

    def test_entity_flag_full_initialization(self):
        """Test full initialization of EntityFlag with all possible parameters."""
        entity_flag = EntityFlag(
            flag_name="test_flag",
            flag_value=True,
            id=1,
            primary_entity_id=2,
            ref_entity_id=3
        )
        self.assertEqual(entity_flag.flag_name, "test_flag")
        self.assertTrue(entity_flag.flag_value)
        self.assertEqual(entity_flag.id, 1)
        self.assertEqual(entity_flag.primary_entity_id, 2)
        self.assertEqual(entity_flag.ref_entity_id, 3)
        self.assertTrue(entity_flag.is_persisted)
from unittest import TestCase

from codiet.model.units.unit import Unit

class TestUnit(TestCase):
    
        def setUp(self) -> None:
            pass
    
        def test_init(self):
            """Check a unit can be initialised."""
            # Create a new unit object
            unit = Unit(
                unit_name="test",
                single_display_name="Test",
                plural_display_name="Tests",
                type="test",
                aliases=set(['t'])
            )
    
            # Check the unit name is set correctly
            self.assertEqual(unit.name, "test")
    
            # Check the single display name is set correctly
            self.assertEqual(unit.single_display_name, "Test")
    
            # Check the plural display name is set correctly
            self.assertEqual(unit.plural_display_name, "Tests")
    
            # Check the type is set correctly
            self.assertEqual(unit.type, "test")
    
            # Check the aliases list is set correctly
            self.assertEqual(unit.aliases, frozenset({'t'}))

        def test_equality(self):
            """Check the equality of two Unit objects.
            Two units are considered equal if their unit name and type are the same.
            """
            # Create two identical unit objects
            unit1 = Unit(
                unit_name="test",
                single_display_name="Test",
                plural_display_name="Tests",
                type="test",
                aliases=set(["t"])
            )
            unit2 = Unit(
                unit_name="test",
                single_display_name="Test",
                plural_display_name="Tests",
                type="test",
                aliases=set(["t"])
            )
            unit3 = Unit(
                unit_name="test3",
                single_display_name="Test",
                plural_display_name="Tests",
                type="test",
                aliases=set(["t"])
            )
    
            # Check if the two units are equal
            self.assertEqual(unit1, unit2)

            # Check if the two units are not equal
            self.assertNotEqual(unit1, unit3)
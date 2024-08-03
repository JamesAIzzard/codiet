from unittest import TestCase

from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion

class TestUnitConversion(TestCase):

    def setUp(self) -> None:
        pass

    def test_minimal_init(self):
        """
        Test the minimal initialization of UnitConversion class.
        """
        # Create a Unit object with 'test' as the unit name
        from_unit = Unit('test', 'test', 'tests', 'mass')
        to_unit = Unit('test2', 'test', 'tests', 'mass')
        unit_conversion = UnitConversion(from_unit, to_unit)

        # Check if the from unit is set correctly
        self.assertEqual(unit_conversion.from_unit, from_unit)

        # Check if the to unit is set correctly
        self.assertEqual(unit_conversion.to_unit, to_unit)

        # Check if the from unit quantity is None
        self.assertIsNone(unit_conversion.from_unit_qty)

        # Check if the to unit quantity is None
        self.assertIsNone(unit_conversion.to_unit_qty)

    def test_raises_error_on_identical_units(self):
        """Test if an error is raised when the from and to units are identical."""
        # Create two identical Unit objects with 'test' as the unit name
        from_unit = Unit('test', 'test', 'tests', 'mass')
        to_unit = Unit('test', 'test', 'tests', 'mass')

        # Check if a ValueError is raised when we initialise the UnitConversion object
        with self.assertRaises(ValueError):
            UnitConversion(from_unit, to_unit)

    def test_is_defined(self):
        """Test the is_defined property of UnitConversion class."""
        # Create a Unit object with 'test' as the unit name
        from_unit = Unit('test', 'test', 'tests', 'mass')
        to_unit = Unit('test2', 'test', 'tests', 'mass')
        unit_conversion = UnitConversion(from_unit, to_unit)

        # Check if the is_defined property is False
        self.assertFalse(unit_conversion.is_defined)

        # Set the from unit quantity
        unit_conversion.from_unit_qty = 1

        # Check if the is_defined property is False
        self.assertFalse(unit_conversion.is_defined)

        # Set the to unit quantity
        unit_conversion.to_unit_qty = 1

        # Check if the is_defined property is True
        self.assertTrue(unit_conversion.is_defined)

    def test_ratio(self):
        """Test the ratio property of UnitConversion class."""
        # Create a Unit object with 'test' as the unit name
        from_unit = Unit('test', 'test', 'tests', 'mass')
        to_unit = Unit('test2', 'test', 'tests', 'mass')
        unit_conversion = UnitConversion(from_unit, to_unit)

        # Set the from unit quantity
        unit_conversion.from_unit_qty = 1

        # Set the to unit quantity
        unit_conversion.to_unit_qty = 2

        # Check if the ratio is calculated correctly
        self.assertEqual(unit_conversion.ratio, 2)

    def test_convert_quantity(self):
        """Test the convert_quantity method of UnitConversion class."""
        # Create a Unit object with 'test' as the unit name
        from_unit = Unit('test', 'test', 'tests', 'mass')
        to_unit = Unit('test2', 'test', 'tests', 'mass')
        unit_conversion = UnitConversion(from_unit, to_unit)

        # Set the from unit quantity
        unit_conversion.from_unit_qty = 1

        # Set the to unit quantity
        unit_conversion.to_unit_qty = 2

        # Check if the quantity is converted correctly
        self.assertEqual(unit_conversion.convert_quantity(1), 2)

    def test_reverse_convert_quantity(self):
        """Test the reverse_convert_quantity method of UnitConversion class."""
        # Create a Unit object with 'test' as the unit name
        from_unit = Unit('test', 'test', 'tests', 'mass')
        to_unit = Unit('test2', 'test', 'tests', 'mass')
        unit_conversion = UnitConversion(from_unit, to_unit)

        # Set the from unit quantity
        unit_conversion.from_unit_qty = 1

        # Set the to unit quantity
        unit_conversion.to_unit_qty = 2

        # Check if the quantity is converted correctly
        self.assertEqual(unit_conversion.reverse_convert_quantity(2), 1)

    def test_equality(self):
        """Test the equality of two UnitConversion objects."""
        # Create two identical UnitConversion objects
        from_unit = Unit('test', 'test', 'tests', 'mass')
        to_unit = Unit('test2', 'test', 'tests', 'mass')
        unit_conversion1 = UnitConversion(from_unit, to_unit)
        unit_conversion2 = UnitConversion(from_unit, to_unit)

        # Check if the two unit conversions are equal
        self.assertEqual(unit_conversion1, unit_conversion2)
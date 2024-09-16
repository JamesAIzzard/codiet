from unittest import TestCase

from codiet.utils.map import Map
from codiet.model.units.unit import Unit
from codiet.model.units.unit_conversion import UnitConversion

class TestBaseUnitConversion(TestCase):
        
        def setUp(self) -> None:
            # Import the global units
            self.global_units = read_units_from_json()
            # Map them to their names
            self.named_global_units = Map[str, Unit]()
            for global_unit in self.global_units:
                self.named_global_units.add_mapping(global_unit.unit_name, global_unit)

            # Init a test unit conversion
            self.defined_unit_conversion = UnitConversion(
                from_unit=self.named_global_units.get_value('gram'),
                to_unit=self.named_global_units.get_value('kilogram'),
                from_unit_qty=1000,
                to_unit_qty=1
            )

            # Init an undefined unit conversion
            self.undefined_unit_conversion = UnitConversion(
                from_unit=self.named_global_units.get_value('gram'),
                to_unit=self.named_global_units.get_value('kilogram'),
            )
        
        def test_init(self):
            """Check a base unit conversion can be initialised."""
            # Check everything was set up correctly on the defined unit conversion
            self.assertEqual(self.defined_unit_conversion.from_unit, self.named_global_units.get_value('gram'))
            self.assertEqual(self.defined_unit_conversion.to_unit, self.named_global_units.get_value('kilogram'))
            self.assertEqual(self.defined_unit_conversion.from_unit_qty, 1000)
            self.assertEqual(self.defined_unit_conversion.to_unit_qty, 1)

            # Check everything was set up correctly on the undefined unit conversion
            self.assertEqual(self.undefined_unit_conversion.from_unit, self.named_global_units.get_value('gram'))
            self.assertEqual(self.undefined_unit_conversion.to_unit, self.named_global_units.get_value('kilogram'))
            self.assertIsNone(self.undefined_unit_conversion.from_unit_qty)
            self.assertIsNone(self.undefined_unit_conversion.to_unit_qty)

        def test_raises_error_on_identical_units(self):
            """Test if an error is raised when the from and to units are identical."""
            # Create a Unit object with 'test' as the unit name
            unit = self.named_global_units.get_value('gram')
            with self.assertRaises(ValueError):
                UnitConversion(
                    from_unit=unit,
                    to_unit=unit,
                )

        def test_units(self):
            """Test the units property of UnitConversion class."""
            # Check if the units are returned correctly
            self.assertIn(self.defined_unit_conversion.from_unit, self.defined_unit_conversion.units)
            self.assertIn(self.defined_unit_conversion.to_unit, self.defined_unit_conversion.units)

        def test_ratio(self):
            """Test the ratio property of UnitConversion class."""
            # Check if the ratio is calculated correctly
            self.assertEqual(self.defined_unit_conversion.ratio, 1 / 1000)

        def test_convert_quantity(self):
            """Test the convert_quantity method of UnitConversion class."""
            # Check if the quantity is converted correctly
            self.assertEqual(self.defined_unit_conversion.convert_quantity(1000), 1)

        def test_reverse_convert_quantity(self):
            """Test the reverse_convert_quantity method of UnitConversion class."""
            # Check if the quantity is converted correctly
            self.assertEqual(self.defined_unit_conversion.reverse_convert_quantity(1), 1000)

        def test_equality(self):
            """Test the equality of two UnitConversion objects."""
            # Create two identical unit conversion objects
            unit_conversion1 = UnitConversion(
                from_unit=self.named_global_units.get_value('gram'),
                to_unit=self.named_global_units.get_value('kilogram'),
                from_unit_qty=1000,
                to_unit_qty=1
            )
            unit_conversion2 = UnitConversion(
                from_unit=self.named_global_units.get_value('gram'),
                to_unit=self.named_global_units.get_value('kilogram'),
                from_unit_qty=1000,
                to_unit_qty=1
            )
            unit_conversion3 = UnitConversion(
                from_unit=self.named_global_units.get_value('gram'),
                to_unit=self.named_global_units.get_value('millilitre'),
                from_unit_qty=1,
                to_unit_qty=1
            )

            # Check if the two unit conversions are equal
            self.assertEqual(unit_conversion1, unit_conversion2)
            self.assertNotEqual(unit_conversion1, unit_conversion3)
            self.assertNotEqual(unit_conversion2, unit_conversion3)                
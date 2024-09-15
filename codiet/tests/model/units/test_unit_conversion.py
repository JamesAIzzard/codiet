from unittest import TestCase

from codiet.db_population.units import read_units_from_json
from codiet.utils.map import Map
from codiet.model.units.unit import Unit
from codiet.model.units.global_unit_conversion import GlobalUnitConversion

class TestUnitConversion(TestCase):

    def setUp(self) -> None:
        # Import the global units
        self.global_units = read_units_from_json()
        # Map them to their names
        self.named_global_units = Map[str, Unit]()
        for global_unit in self.global_units:
            self.named_global_units.add_mapping(global_unit.unit_name, global_unit)

        # Init a test unit conversion
        self.unit_conversion = GlobalUnitConversion(
            from_unit=self.named_global_units.get_value('gram'),
            to_unit=self.named_global_units.get_value('kilogram'),
            from_unit_qty=1000,
            to_unit_qty=1
        )

    def test_init(self):
        """Test initialisation."""
        # Check everything was set up correctly
        self.assertEqual(self.unit_conversion.from_unit, self.named_global_units.get_value('gram'))
        self.assertEqual(self.unit_conversion.to_unit, self.named_global_units.get_value('kilogram'))
        self.assertEqual(self.unit_conversion.from_unit_qty, 1000)
        self.assertEqual(self.unit_conversion.to_unit_qty, 1)

    def test_from_unit_qty_not_settable(self):
        """Test that from_unit_qty is not settable."""
        with self.assertRaises(AttributeError):
            self.unit_conversion.from_unit_qty = 1 # type: ignore # testing this

    def test_to_unit_qty_not_settable(self):
        """Test that to_unit_qty is not settable."""
        with self.assertRaises(AttributeError):
            self.unit_conversion.to_unit_qty = 1 # type: ignore # testing this
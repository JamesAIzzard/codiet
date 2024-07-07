import unittest

from codiet.models.units import Unit, UnitConversion, IngredientUnitConversion, get_available_units

class TestUnitConversion(unittest.TestCase):

    def setUp(self):
        # Set up example data
        self.global_units = {
            1: Unit(1, "grams", "gram", "grams", "mass"),
            2: Unit(2, "kilograms", "kilogram", "kilograms", "mass"),
            3: Unit(3, "litres", "litre", "litres", "volume"),
            4: Unit(4, "cups", "cup", "cups", "volume"),
            5: Unit(5, "millilitres", "millilitre", "millilitres", "volume"),
            6: Unit(6, "slices", "slice", "slices", "grouping"),
            7: Unit(7, "pieces", "piece", "pieces", "grouping")
        }
        self.global_unit_conversions = {
            1: UnitConversion(1, 1, 2, 1, 0.001),  # grams to kilograms
            2: UnitConversion(2, 3, 5, 1, 1000),  # litres to millilitres
            3: UnitConversion(3, 4, 5, 1, 250)  # cups to millilitres
        }
        self.ingredient_unit_conversions = {
            1: IngredientUnitConversion(1, 1, 1, 5, 1, 1),  # grams to millilitres for ingredient 1
            2: IngredientUnitConversion(2, 1, 1, 6, 6, 2)  # grams to slices for ingredient 1
        }

    def test_can_get_correct_units_from_grams(self):
        # Test getting all units from grams
        root_unit = self.global_units[1]
        available_units = get_available_units(
            root_unit,
            self.global_units,
            self.global_unit_conversions,
            self.ingredient_unit_conversions
        )
        # Check there is the right number
        self.assertEqual(len(available_units), 6)
        # Check the right units are there
        self.assertIn(1, available_units)
        self.assertIn(2, available_units)
        self.assertIn(3, available_units)
        self.assertIn(4, available_units)
        self.assertIn(5, available_units)
        self.assertIn(6, available_units)

import unittest

from codiet.models.units import (
    Unit,
    UnitConversion,
    IngredientUnitConversion,
    IngredientUnitsSystem,
)

class TestIngredientUnitsSystem(unittest.TestCase):

    def setUp(self):
        # Set up test data
        self.global_units = {
            1: Unit(1, "grams", "gram", "grams", "mass"),
            2: Unit(2, "kilograms", "kilogram", "kilograms", "mass"),
            3: Unit(3, "litres", "litre", "litres", "volume"),
            4: Unit(4, "millilitres", "millilitre", "millilitres", "volume"),
            5: Unit(5, "cups", "cup", "cups", "volume"),
            6: Unit(6, "slices", "slice", "slices", "grouping")
        }
        
        self.global_unit_conversions = {
            1: UnitConversion(1, 1, 2, 1000, 1),  # 1000 grams = 1 kilogram
            2: UnitConversion(2, 3, 4, 1, 1000),  # 1 litre = 1000 millilitres
            3: UnitConversion(3, 4, 5, 250, 1),   # 250 millilitres = 1 cup
        }
        
        self.ingredient_unit_conversions = {
            1: IngredientUnitConversion(1, 1, 1, 6, 100, 1)  # 100 grams = 1 slice (for ingredient 1)
        }
        
        # Create a system with disconnected graph
        self.disconnected_system = IngredientUnitsSystem(
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions,
            ingredient_unit_conversions=self.ingredient_unit_conversions
        )

        # Create a system with connected graph
        connected_conversions = self.global_unit_conversions.copy()
        connected_conversions[4] = UnitConversion(4, 1, 4, 1, 1)  # 1 gram = 1 millilitre (for testing purposes)
        self.connected_system = IngredientUnitsSystem(
            global_units=self.global_units,
            global_unit_conversions=connected_conversions,
            ingredient_unit_conversions=self.ingredient_unit_conversions
        )

    def test_init(self):
        self.assertIsInstance(self.disconnected_system, IngredientUnitsSystem)
        self.assertEqual(len(self.disconnected_system.graph), 6)  # All units should be in the graph

    def test_get_conversion_factor_same_unit(self):
        factor = self.disconnected_system.get_conversion_factor(1, 1)
        self.assertEqual(factor, 1.0)

    def test_get_conversion_factor_direct(self):
        factor = self.disconnected_system.get_conversion_factor(1, 2)
        self.assertEqual(factor, 0.001)  # 1 gram = 0.001 kilogram

    def test_get_conversion_factor_reverse(self):
        factor = self.disconnected_system.get_conversion_factor(2, 1)
        self.assertEqual(factor, 1000)  # 1 kilogram = 1000 grams

    def test_get_conversion_factor_multi_step(self):
        factor = self.disconnected_system.get_conversion_factor(3, 5)
        self.assertEqual(factor, 4)  # 1 litre = 4 cups

    def test_get_conversion_factor_ingredient_specific(self):
        factor = self.disconnected_system.get_conversion_factor(1, 6)
        self.assertEqual(factor, 0.01)  # 1 gram = 0.01 slices

    def test_convert_units(self):
        result = self.disconnected_system.convert_units(500, 1, 2)
        self.assertEqual(result, 0.5)  # 500 grams = 0.5 kilograms

    def test_convert_units_multi_step(self):
        result = self.disconnected_system.convert_units(2, 3, 5)
        self.assertEqual(result, 8)  # 2 litres = 8 cups

    def test_get_available_units_disconnected(self):
        available_units = self.disconnected_system.get_available_units(1)
        self.assertEqual(len(available_units), 3)  # Only mass units and slices should be reachable

    def test_get_available_units_connected(self):
        available_units = self.connected_system.get_available_units(1)
        self.assertEqual(len(available_units), 6)  # All units should be reachable

    def test_update_graph(self):
        new_conversion = UnitConversion(5, 2, 3, 1, 1)  # 1 kilogram = 1 litre (nonsensical, but for testing)
        self.disconnected_system.update_graph(global_unit_conversions={5: new_conversion})
        factor = self.disconnected_system.get_conversion_factor(2, 3)
        self.assertEqual(factor, 1)  # Check if the new conversion is applied

    def test_path_caching_connected(self):
        # First conversion (should calculate and cache the path)
        self.connected_system.get_conversion_factor(1, 5)
        
        # Modify the graph directly (this is not recommended in practice, but useful for testing)
        self.connected_system.graph[1][5] = 0.5
        
        # Second conversion (should use the cached path and not reflect the graph change)
        factor = self.connected_system.get_conversion_factor(1, 5)
        self.assertNotEqual(factor, 0.5)

    def test_clear_path_cache_connected(self):
        # First conversion (should calculate and cache the path)
        self.connected_system.get_conversion_factor(1, 5)
        
        # Clear the cache
        self.connected_system.clear_path_cache()
        
        # Modify the graph directly
        self.connected_system.graph[1][5] = 0.5
        
        # Conversion after clearing cache (should reflect the graph change)
        factor = self.connected_system.get_conversion_factor(1, 5)
        self.assertEqual(factor, 0.5)

    def test_conversion_path_not_found_disconnected(self):
        with self.assertRaises(ValueError):
            self.disconnected_system.get_conversion_factor(1, 5)  # No path from grams to cups in disconnected graph

    def test_conversion_path_found_connected(self):
        try:
            self.connected_system.get_conversion_factor(1, 5)
        except ValueError:
            self.fail("get_conversion_factor raised ValueError unexpectedly!")

    def test_conversion_path_not_found_invalid_unit(self):
        with self.assertRaises(ValueError):
            self.connected_system.get_conversion_factor(1, 99)  # 99 is not a valid unit ID
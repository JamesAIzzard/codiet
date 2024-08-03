import unittest

from codiet.db_population.units import read_global_units_from_json
from codiet.db_population.units import read_global_unit_conversions_from_json
from codiet.utils.map import Map
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.entity_unit_conversion import EntityUnitConversion
from codiet.models.units.entity_units_system import EntityUnitsSystem

class TestEntityUnitsSystem(unittest.TestCase):

    def setUp(self):
        # Grab all the global units and conversions
        self.global_units = read_global_units_from_json()
        self.global_unit_conversions = read_global_unit_conversions_from_json()

        # Map the units to their names
        self.named_global_units = Map[str, Unit]()
        for global_unit in self.global_units:
            self.named_global_units.add_mapping(global_unit.unit_name, global_unit)

        
        # Create a system with disconnected graph
        self.disconnected_system = EntityUnitsSystem(
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions,
            entity_unit_conversions=self.entity_unit_conversions
        )

        # Create a system with connected graph
        connected_conversions = self.global_unit_conversions.copy()
        connected_conversions.append(UnitConversion(self.gram, self.millilitre, 1, 1))  # 1 gram = 1 millilitre (for testing purposes)
        self.connected_system = EntityUnitsSystem(
            global_units=self.global_units,
            global_unit_conversions=connected_conversions,
            entity_unit_conversions=self.entity_unit_conversions
        )

    def test_conversion_factor_same_unit(self):
        factor = self.disconnected_system.get_conversion_factor(self.gram, self.gram)
        self.assertEqual(factor, 1.0)

    def test_conversion_factor_direct(self):
        factor = self.disconnected_system.get_conversion_factor(self.gram, self.kilogram)
        self.assertEqual(factor, 0.001)  # 1 gram = 0.001 kilogram

    def test_conversion_factor_reverse(self):
        factor = self.disconnected_system.get_conversion_factor(self.kilogram, self.gram)
        self.assertEqual(factor, 1000)  # 1 kilogram = 1000 grams

    def test_conversion_factor_multi_step(self):
        factor = self.disconnected_system.get_conversion_factor(self.litre, self.cup)
        self.assertEqual(factor, 4)  # 1 litre = 4 cups

    def test_conversion_factor_entity_specific(self):
        factor = self.disconnected_system.get_conversion_factor(self.gram, self.slice)
        self.assertEqual(factor, 0.01)  # 1 gram = 0.01 slices

    def test_convert_units(self):
        result = self.disconnected_system.convert_units(500, self.gram, self.kilogram)
        self.assertEqual(result, 0.5)  # 500 grams = 0.5 kilograms

    def test_convert_units_multi_step(self):
        result = self.disconnected_system.convert_units(2, self.litre, self.cup)
        self.assertEqual(result, 8)  # 2 litres = 8 cups

    def test_get_available_units_disconnected(self):
        available_units = self.disconnected_system.get_available_units(self.gram)
        self.assertEqual(len(available_units), 3)  # Only mass units and slices should be reachable

    def test_get_available_units_connected(self):
        available_units = self.connected_system.get_available_units(self.gram)
        self.assertEqual(len(available_units), 6)  # All units should be reachable

    def test_get_available_units_default(self):
        available_units = self.disconnected_system.get_available_units()
        self.assertEqual(len(available_units), 3)  # Only mass units and slices should be reachable

    def test_path_caching(self):
        # First conversion (should calculate and cache the path)
        self.connected_system.get_conversion_factor(self.gram, self.cup)
        
        # Modify the graph directly (this is not recommended in practice, but useful for testing)
        self.connected_system._graph[self.gram][self.cup] = 0.5
        
        # Second conversion (should use the cached path and not reflect the graph change)
        factor = self.connected_system.get_conversion_factor(self.gram, self.cup)
        self.assertNotEqual(factor, 0.5)

    def test_clear_path_cache(self):
        # First conversion (should calculate and cache the path)
        self.connected_system.get_conversion_factor(self.gram, self.cup)
        
        # Clear the cache
        self.connected_system.clear_path_cache()
        
        # Modify the graph directly
        self.connected_system._graph[self.gram][self.cup] = 0.5
        
        # Conversion after clearing cache (should reflect the graph change)
        factor = self.connected_system.get_conversion_factor(self.gram, self.cup)
        self.assertEqual(factor, 0.5)

    def test_conversion_path_not_found_disconnected(self):
        with self.assertRaises(ValueError):
            self.disconnected_system.get_conversion_factor(self.gram, self.cup)  # No path from grams to cups in disconnected graph

    def test_conversion_path_found_connected(self):
        try:
            self.connected_system.get_conversion_factor(self.gram, self.cup)
        except ValueError:
            self.fail("get_conversion_factor raised ValueError unexpectedly!")

    def test_conversion_path_not_found_invalid_unit(self):
        invalid_unit = Unit("invalid", "invalid", "invalids", "invalid")
        with self.assertRaises(ValueError):
            self.connected_system.get_conversion_factor(self.gram, invalid_unit)

    def test_entity_unit_conversion_update(self):
        # Set up a simple system with one entity unit conversion
        units = [self.gram, self.slice]
        global_conversions = []
        entity_conversions = [EntityUnitConversion(self.gram, self.slice, 10, 1)]  # 10 grams = 1 slice
        
        system = EntityUnitsSystem(units, global_conversions, entity_conversions)
        
        # Initial conversion
        initial_result = system.convert_units(100, self.gram, self.slice)  # Convert 100 grams to slices
        self.assertEqual(initial_result, 10)  # 100 grams should be 10 slices
        
        # Update the entity unit conversion
        new_entity_conversions = [EntityUnitConversion(self.gram, self.slice, 20, 1)]  # Now 20 grams = 1 slice
        system.set_entity_unit_conversions(new_entity_conversions)
        
        # Conversion after update
        updated_result = system.convert_units(100, self.gram, self.slice)  # Convert 100 grams to slices again
        self.assertEqual(updated_result, 5)  # Now 100 grams should be 5 slices
        
        # Verify that the reverse conversion also works correctly
        reverse_result = system.convert_units(1, self.slice, self.gram)  # Convert 1 slice to grams
        self.assertEqual(reverse_result, 20)  # 1 slice should now be 20 grams

    def test_rescale_quantity(self):
        # Test the rescale_quantity method: 10g protein in 100g ingredient, scaled to 200g ingredient
        result = self.connected_system.rescale_quantity(
            ref_from_unit=self.gram,  # grams (ingredient)
            ref_to_unit=self.gram,    # grams (protein)
            ref_from_quantity=100,
            ref_to_quantity=10,
            quantity=200
        )
        self.assertAlmostEqual(result, 20, places=2)

    def test_rescale_quantity_different_units(self):
        # Test with different units: 10g protein in 0.1kg ingredient, scaled to 0.3kg ingredient
        result = self.connected_system.rescale_quantity(
            ref_from_unit=self.kilogram,  # kilograms (ingredient)
            ref_to_unit=self.gram,        # grams (protein)
            ref_from_quantity=0.1,
            ref_to_quantity=10,
            quantity=0.3
        )
        self.assertAlmostEqual(result, 30, places=2)
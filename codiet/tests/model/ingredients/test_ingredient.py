from unittest import TestCase

from codiet.utils.map import Map
from codiet.db_population.units import read_global_units_from_json, read_global_unit_conversions_from_json
from codiet.db_population.flags import read_global_flags_from_json
from codiet.db_population.nutrients import read_global_nutrients_from_json
from codiet.models.units.unit import Unit
from codiet.models.nutrients.nutrient import Nutrient
from codiet.models.units.ingredient_unit_conversion import IngredientUnitConversion
from codiet.models.flags.flag import Flag
from codiet.models.nutrients.ingredient_nutrient_quantity import IngredientNutrientQuantity
from codiet.models.ingredients.ingredient import Ingredient


class TestIngredient(TestCase):

    def setUp(self):
        # Cache the global units
        self.global_units = read_global_units_from_json()
        self.global_unit_conversions = read_global_unit_conversions_from_json()
        # Map the units to their names
        self.named_global_units = Map[str, Unit]()
        for global_unit in self.global_units:
            self.named_global_units.add_mapping(global_unit.unit_name, global_unit)

        # Cache the global flags
        self.global_flags = read_global_flags_from_json()
        # Map the flags to their names
        self.named_global_flags = Map[str, Flag]()
        for global_flag in self.global_flags:
            self.named_global_flags.add_mapping(global_flag.flag_name, global_flag)

        # Cache the global nutrients
        self.global_nutrients = read_global_nutrients_from_json()
        # Map the nutrients to their names
        self.named_global_nutrients = Map[str, Nutrient]()
        for global_nutrient in self.global_nutrients:
            self.named_global_nutrients.add_mapping(global_nutrient.nutrient_name, global_nutrient)

        # Create a test ingredient
        self.ingredient = Ingredient(
            name="Test Ingredient",
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions
        )

    def test_name(self):
        """Test the name property."""
        # Check the ingredient instance has the correct name
        self.assertEqual(self.ingredient.name, "Test Ingredient")

    def test_description(self):
        """Test the description property."""
        # Check the description is None to start
        self.assertIsNone(self.ingredient.description)
        # Check we can set it
        self.ingredient.description = "Test Description"
        self.assertEqual(self.ingredient.description, "Test Description")

    def test_standard_unit(self):
        """Test the standard unit property."""
        # Check the standard unit is grams to start
        self.assertEqual(self.ingredient.standard_unit, self.named_global_units.get_value("gram"))

    def test_cant_init_with_unset_units(self):
        """Test that we can't initialise an ingredient without a standard unit."""
        # Check we can't initialise with unset standard unit
        with self.assertRaises(ValueError):
            Ingredient(
                name="Test Ingredient",
                global_units=self.global_units,
                global_unit_conversions=self.global_unit_conversions,
                standard_unit=self.named_global_units.get_value("millilitre")
            )
        
        # Check we can't initialise with unset cost unit
        with self.assertRaises(ValueError):
            Ingredient(
                name="Test Ingredient",
                global_units=self.global_units,
                global_unit_conversions=self.global_unit_conversions,
                cost_qty_unit=self.named_global_units.get_value("millilitre")
            )

    def test_cant_change_standard_unit_to_unset_unit(self):
        """Test that we can't change the standard unit to an unset unit."""
        # Check we can't change the standard unit to an unset unit
        with self.assertRaises(ValueError):
            self.ingredient.standard_unit = self.named_global_units.get_value("millilitre")
        
    def test_cost_value(self):
        """Test the cost value property."""
        # Check the cost value is None to start
        self.assertIsNone(self.ingredient.cost_value)
        # Check we can set it
        self.ingredient.cost_value = 1.0
        self.assertEqual(self.ingredient.cost_value, 1.0)

    def test_cost_qty_unit(self):
        """Test the cost quantity unit property."""
        # Check the cost quantity unit is the standard unit to start
        self.assertEqual(self.ingredient.cost_qty_unit, self.named_global_units.get_value("gram"))

        # Check we can update it
        self.ingredient.cost_qty_unit = self.named_global_units.get_value("kilogram")
        self.assertEqual(self.ingredient.cost_qty_unit, self.named_global_units.get_value("kilogram"))

    def test_cant_change_cost_unit_to_unset_unit(self):
        """Test that we can't change the cost unit to an unset unit."""
        # Check we can't change the cost unit to an unset unit
        with self.assertRaises(ValueError):
            self.ingredient.cost_qty_unit = self.named_global_units.get_value("millilitre")

    def test_cost_qty_value(self):
        """Test the cost quantity value property."""
        # Check the cost quantity value is None to start
        self.assertIsNone(self.ingredient.cost_qty_value)
        # Check we can set it
        self.ingredient.cost_qty_value = 1.0
        self.assertEqual(self.ingredient.cost_qty_value, 1.0)

    
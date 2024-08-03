from unittest import TestCase
from codiet.db_population.units import read_global_units_from_json, read_global_unit_conversions_from_json
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
        self.gram_unit = next(unit for unit in self.global_units if unit.unit_name == 'gram')
        self.global_unit_conversions = read_global_unit_conversions_from_json()

    def test_name(self):
        """Test the name property."""
        # Create an ingredient instance
        ingredient = Ingredient(name="Test Ingredient")
        self.assertEqual(ingredient.name, "Test Ingredient")
        with self.assertRaises(ValueError):
            ingredient.name = ""
        with self.assertRaises(ValueError):
            ingredient.name = "   "

    def test_standard_unit_id(self):
        """Test the standard unit property."""
        # Create an ingredient and pass in gram unit
        ingredient = Ingredient(
            name="Test Ingredient",
            standard_unit=self.gram_unit
        )

        # Check it is set to gram to start
        self.assertEqual(ingredient.standard_unit, self.gram_unit)

        # Check we can't set it to None
        with self.assertRaises(ValueError):
            ingredient.standard_unit = None # type: ignore # this is what the test is checking

        # Check we can change it
        # TODO: Check we can't set it to a unit that isn't available

    def test_unit_conversions(self):
        """Test the unit conversions property."""
        ingredient = Ingredient(name="Test Ingredient")
        # Check it is empty to start
        self.assertEqual(ingredient.unit_conversions, set())

        # Add a conversion
        

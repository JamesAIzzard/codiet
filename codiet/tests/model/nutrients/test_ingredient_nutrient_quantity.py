from unittest import TestCase

from codiet.db_population.nutrients import read_global_nutrients_from_json
from codiet.utils.map import Map
from codiet.model.nutrients.nutrient import Nutrient
from codiet.model.units.unit import Unit
from codiet.model.nutrients.nutrient_quantity import NutrientQuantity
from codiet.model.ingredients.ingredient import Ingredient

class TestIngredientNutrientQuantity(TestCase):
    def setUp(self):
        # Grab all the global nutrients and units
        self.global_nutrients = read_global_nutrients_from_json()
        self.global_units = read_units_from_json()
        self.global_unit_conversions = read_global_unit_conversions_from_json()

        # Map the nutrients to their names
        self.named_global_nutrients = Map[str, Nutrient]()
        for global_nutrient in self.global_nutrients:
            self.named_global_nutrients.add_mapping(global_nutrient.name, global_nutrient)

        # Map the units to their names
        self.named_global_units = Map[str, Unit]()
        for global_unit in self.global_units:
            self.named_global_units.add_mapping(global_unit.unit_name, global_unit)

        # Create a test ingredient
        self.ingredient = Ingredient(
            name="Test Ingredient",
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions,
        )

    def test_init(self):
        """Check that we can initialise an instance."""
        enq = NutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value('protein'),
            nutrient_mass_unit=self.named_global_units.get_value('gram'),
            nutrient_mass_value=10.0,
            ingredient_grams_value=100.0
        )
        
        # Check the instance
        self.assertEqual(enq.ingredient, self.ingredient)
        self.assertEqual(enq.nutrient, self.named_global_nutrients.get_value('protein'))
        self.assertEqual(enq.nutrient_mass_unit, self.named_global_units.get_value('gram'))
        self.assertEqual(enq.nutrient_mass_value, 10.0)
        self.assertEqual(enq.ingredient_grams_qty, 100.0)

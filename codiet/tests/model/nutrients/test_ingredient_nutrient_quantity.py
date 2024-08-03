from unittest import TestCase

from codiet.db_population.nutrients import read_global_nutrients_from_json
from codiet.db_population.units import read_global_units_from_json
from codiet.utils.map import Map
from codiet.models.nutrients.nutrient import Nutrient
from codiet.models.units.unit import Unit
from codiet.models.nutrients.ingredient_nutrient_quantity import IngredientNutrientQuantity
from codiet.models.ingredients.ingredient import Ingredient

class TestIngredientNutrientQuantity(TestCase):
    def setUp(self):
        # Grab all the global nutrients and units
        self.global_nutrients = read_global_nutrients_from_json()
        self.global_units = read_global_units_from_json()

        # Map the nutrients to their names
        self.named_global_nutrients = Map[str, Nutrient]()
        for global_nutrient in self.global_nutrients:
            self.named_global_nutrients.add_mapping(global_nutrient.nutrient_name, global_nutrient)

        # Map the units to their names
        self.named_global_units = Map[str, Unit]()
        for global_unit in self.global_units:
            self.named_global_units.add_mapping(global_unit.unit_name, global_unit)

        # Create a test ingredient
        self.ingredient = Ingredient(
            name="Test Ingredient",
        )

    def test_init(self):
        """Check that we can initialise an instance."""
        enq = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value('protein'),
            ntr_mass_unit=self.named_global_units.get_value('gram'),
            ntr_mass_value=10.0,
            entity_grams_qty=100.0
        )
        
        # Check the instance
        self.assertEqual(enq.ingredient, self.ingredient)
        self.assertEqual(enq.nutrient, self.named_global_nutrients.get_value('protein'))
        self.assertEqual(enq.ntr_mass_unit, self.named_global_units.get_value('gram'))
        self.assertEqual(enq.ntr_mass_value, 10.0)
        self.assertEqual(enq.entity_grams_qty, 100.0)

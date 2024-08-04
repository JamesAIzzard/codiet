from unittest import TestCase

from codiet.db_population.units import read_global_units_from_json, read_global_unit_conversions_from_json
from codiet.models.flags.ingredient_flag import IngredientFlag
from codiet.models.ingredients.ingredient import Ingredient

class TestIngredientFlag(TestCase):
    def setUp(self) -> None:
        # Cache the global units and unit conversions
        self.global_units = read_global_units_from_json()
        self.global_unit_conversions = read_global_unit_conversions_from_json()

        self.ingredient = Ingredient(
            name="Test Ingredient",
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions
        )

    def test_init(self):
        """Test the initialisation of IngredientFlag."""
        # Check we can initialise without a value
        ingredient_flag = IngredientFlag(
            ingredient=self.ingredient,
            flag_name="Test Flag"
        )
        self.assertEqual(ingredient_flag.ingredient, self.ingredient)
        self.assertEqual(ingredient_flag.flag_name, "Test Flag")
        self.assertFalse(ingredient_flag.flag_value)

        # Check we can initialise with a value
        ingredient_flag = IngredientFlag(
            ingredient=self.ingredient,
            flag_name="Test Flag",
            flag_value=True
        )
        self.assertEqual(ingredient_flag.ingredient, self.ingredient)
        self.assertEqual(ingredient_flag.flag_name, "Test Flag")
        self.assertTrue(ingredient_flag.flag_value)
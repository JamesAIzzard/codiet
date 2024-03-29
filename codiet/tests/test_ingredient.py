from unittest import TestCase

from codiet.models.ingredient import Ingredient

class TestIngredientInstantiation(TestCase):
    def test_ingredient_instantiation(self):
        ingredient = Ingredient(name="test")
        self.assertIsInstance(ingredient, Ingredient)

class TestIngredientPopulatedNutrients(TestCase):
    def test_ingredient_populated_nutrients(self):
        # Create an ingredient
        ingredient = Ingredient(name="test")
        ingredient.nutrients = {
            "test_nutrient": {
                "ntr_qty": 1.0,
                "ntr_qty_unit": "g",
                "ing_qty": 1.0,
                "ing_qty_unit": "g",
            },
            "test_nutrient_2": {
                "ntr_qty": 1.0,
                "ntr_qty_unit": "g",
                "ing_qty": 1.0,
                "ing_qty_unit": "g",
            }
        }
        self.assertEqual(ingredient.populated_nutrients, ["test_nutrient", "test_nutrient_2"])

class TestIngredientNutrientIsPopulated(TestCase):
    def test_ingredient_nutrient_is_populated_true(self):
        ingredient = Ingredient(name="test")
        ingredient.nutrients = {
            "test_nutrient": {
                "ntr_qty": 1.0,
                "ntr_qty_unit": "g",
                "ing_qty": 1.0,
                "ing_qty_unit": "g",
            }
        }
        self.assertTrue(ingredient.nutrient_is_populated("test_nutrient"))
    
    def test_ingredient_nutrient_is_populated_false(self):
        ingredient = Ingredient(name="test")
        self.assertFalse(ingredient.nutrient_is_populated("test_nutrient"))
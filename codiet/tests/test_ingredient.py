from unittest import TestCase

from codiet.models.ingredient import Ingredient

class TestIngredientInstantiation(TestCase):
    def test_ingredient_instantiation(self):
        ingredient = Ingredient(name="test")
        self.assertIsInstance(ingredient, Ingredient)
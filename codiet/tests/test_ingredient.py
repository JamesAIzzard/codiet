from unittest import TestCase

from codiet.models.ingredient import Ingredient

class TestIngredientInstantiation(TestCase):
    def test_ingredient_instantiation(self):
        ingredient = Ingredient()
        self.assertIsInstance(ingredient, Ingredient)
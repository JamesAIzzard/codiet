from unittest import TestCase

from codiet.models.flags.ingredient_flag import IngredientFlag
from codiet.models.ingredients.ingredient import Ingredient
from codiet.db.stored_entity import StoredEntity

class TestIngredientFlag(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient(
            name="Test Ingredient",
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
from unittest import TestCase, mock

from codiet.db_population.units import read_units_from_json, read_global_unit_conversions_from_json
from codiet.models.flags.ingredient_flag import IngredientFlag
from codiet.models.flags.flag import Flag
from codiet.models.ingredients.ingredient import Ingredient

class TestIngredientFlag(TestCase):
    def setUp(self) -> None:
        # Create a mock ingredient
        self.mock_ingredient = mock.MagicMock(spec=Ingredient)
        self.mock_ingredient.id = 1

        # Create a couple of flags
        self.vegan_flag = Flag(flag_name="Vegan")
        self.halal_flag = Flag(flag_name="Halal")

    def test_init(self):
        """Test the initialisation of IngredientFlag."""
        # Check we can initialise without a value
        ingredient_flag = IngredientFlag(
            ingredient=self.mock_ingredient,
            flag=self.vegan_flag
        )
        self.assertEqual(ingredient_flag.ingredient.id, self.mock_ingredient.id)
        self.assertEqual(ingredient_flag.flag_name, "Vegan")
        self.assertFalse(ingredient_flag.flag_value)

        # Check we can initialise with a value
        ingredient_flag = IngredientFlag(
            ingredient=self.mock_ingredient,
            flag=self.halal_flag,
            flag_value=True
        )
        self.assertEqual(ingredient_flag.ingredient.id, self.mock_ingredient.id)
        self.assertEqual(ingredient_flag.flag_name, "Halal")
        self.assertTrue(ingredient_flag.flag_value)

    def test_value_setter(self):
        """Test the setter for flag_value."""
        # Create an ingredient flag
        ingredient_flag = IngredientFlag(
            ingredient=self.mock_ingredient,
            flag=self.vegan_flag
        )

        # Check it initialised with False
        self.assertFalse(ingredient_flag.flag_value)

        # Set the value to True
        ingredient_flag.flag_value = True

        # Check the value is True
        self.assertTrue(ingredient_flag.flag_value)    
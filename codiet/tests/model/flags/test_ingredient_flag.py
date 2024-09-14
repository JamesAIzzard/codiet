"""Tests for the IngredientFlag class."""
from unittest import TestCase

from codiet.tests.fixtures import IngredientTestFixtures, FlagTestFixtures, UnitsTestFixtures
from codiet.model.flags.ingredient_flag import IngredientFlag

class TestIngredientFlag(TestCase):
    """Tests for the IngredientFlag class."""
    def setUp(self) -> None:
        self.unit_fixtures = UnitsTestFixtures()
        self.ingredient_fixtures = IngredientTestFixtures(
            units_test_fixtures=self.unit_fixtures
        )
        self.flag_fixtures = FlagTestFixtures()

    def test_init(self):
        """Check we can create IngredientFlag instances in the right ways."""
        # Check we can initialise without a value
        ingredient_flag = IngredientFlag(
            flag_name="vegan",
            ingredient=self.ingredient_fixtures.ingredients["apple"],
        )
        self.assertEqual(ingredient_flag.ingredient, self.ingredient_fixtures.ingredients["apple"])
        self.assertEqual(ingredient_flag.flag_name, "vegan")
        self.assertFalse(ingredient_flag.flag_value)

        # Check we can initialise with a value
        ingredient_flag = IngredientFlag(
            flag_name="vegan",
            ingredient=self.ingredient_fixtures.ingredients["apple"],
            value=True
        )
        self.assertEqual(ingredient_flag.ingredient, self.ingredient_fixtures.ingredients["apple"])
        self.assertEqual(ingredient_flag.flag_name, "vegan")
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
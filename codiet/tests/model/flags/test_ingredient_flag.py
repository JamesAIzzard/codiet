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
        self.flag_fixtures = FlagTestFixtures(
            ingredient_fixtures=self.ingredient_fixtures
        )

    def test_init(self):
        """Check we can create IngredientFlag instances in the right ways."""
        # Check we can initialise without a value
        ingredient_flag = IngredientFlag(
            flag_name="vegan",
            ingredient=self.ingredient_fixtures.ingredients["apple"],
        )
        self.assertEqual(ingredient_flag.ingredient, self.ingredient_fixtures.ingredients["apple"])
        self.assertEqual(ingredient_flag.flag_name, "vegan")
        self.assertFalse(ingredient_flag.value)

        # Check we can initialise with a value
        ingredient_flag = IngredientFlag(
            flag_name="vegan",
            ingredient=self.ingredient_fixtures.ingredients["apple"],
            value=True
        )
        self.assertEqual(ingredient_flag.ingredient, self.ingredient_fixtures.ingredients["apple"])
        self.assertEqual(ingredient_flag.flag_name, "vegan")
        self.assertTrue(ingredient_flag.value)

    def test_value_setter(self):
        """Checks the flag_value property is returning the correct value."""
        vegan_flag = self.flag_fixtures.get_ingredient_flag_by_name("vegan")
        vegan_flag.flag_value = False
        self.assertFalse(vegan_flag.flag_value)
        vegan_flag.flag_value = True
        self.assertTrue(vegan_flag.flag_value)

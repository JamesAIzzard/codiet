"""Tests for the ingredient module."""

from unittest import TestCase

from codiet.model.ingredients import Ingredient
from codiet.model.flags import IngredientFlag
from codiet.model.cost import CostRate
from codiet.tests.fixtures import (
    IngredientTestFixtures,
    UnitTestFixtures,
    FlagTestFixtures,
    NutrientTestFixtures,
)


class TestIngredient(TestCase):
    """Test class for the Ingredient class."""

    def setUp(self):
        self.unit_fixtures = UnitTestFixtures()
        self.flag_fixtures = FlagTestFixtures()
        self.nutrient_fixtures = NutrientTestFixtures()
        self.ingredient_fixtures = IngredientTestFixtures(
            units_test_fixtures=self.unit_fixtures
        )

    def test_constructor(self):
        """Checks that the ingredient can be constructed and is an instance of the Ingredient class."""
        apple = Ingredient(name="Apple")
        self.assertIsInstance(apple, Ingredient)

    def test_name(self):
        """Check the name property returns correctly."""
        apple = Ingredient(name="Apple")
        self.assertEqual(apple.name, "Apple")

    def test_description(self):
        """Check that the description property sets and returns correctly."""
        # Check it is set correctly when passed in the constructor
        apple = Ingredient(name="Apple", description="A fruit")
        self.assertEqual(apple.description, "A fruit")

        # Check we can update it
        apple.description = "A fruit that is red"
        self.assertEqual(apple.description, "A fruit that is red")

    def test_standard_unit(self):
        """Test that the standard unit defaults to grams, and that the getter and
        setter works correctly."""
        gram = self.unit_fixtures.get_unit_by_name("gram")
        kilogram = self.unit_fixtures.get_unit_by_name("kilogram")

        # Check the standard unit is grams by default
        apple = Ingredient(name="Apple")
        self.assertEqual(apple.standard_unit, gram)

        # Check we can change it
        apple.standard_unit = self.unit_fixtures.get_unit_by_name("kilogram")
        self.assertEqual(apple.standard_unit, kilogram)

    def test_cant_init_with_unavailable_units(self):
        """Check that we get a value error if we try to initialise
        with a unit that is not available via conversions."""
        # Create an ingredient with a unit that is not available
        with self.assertRaises(ValueError):
            Ingredient(
                name="Apple",
                standard_unit=self.unit_fixtures.get_unit_by_name("millilitre"),
            )

    def test_cant_change_standard_unit_to_unset_unit(self):
        """Check we get an exception if we try and set the standard unit to a unit
        that is not available."""
        apple = Ingredient(name="Apple")

        with self.assertRaises(ValueError):
            apple.standard_unit = self.unit_fixtures.get_unit_by_name("millilitre")

    def test_cost_rate(self):
        """Test the cost rate property."""
        cost_rate = CostRate()
        apple = Ingredient(name="Apple", cost_rate=cost_rate)
        self.assertIs(apple.cost_rate, cost_rate)

    def test_flags(self):
        """Check that the flags property gets and sets flags correctly."""
        apple = Ingredient(name="Apple")

        # Check the flags are empty to start
        self.assertEqual(len(apple.flags), 0)

        # Check we can add a flag
        vegan_flag = self.flag_fixtures.create_ingredient_flag("vegan", apple)
        apple.add_flag(vegan_flag)
        self.assertEqual(len(apple.flags), 1)
        self.assertIn(vegan_flag, apple.flags)

    def test_gi(self):
        """Check the GI property gets and sets the GI correctly."""
        # Check it sets correctly when passed in the constructor
        apple = Ingredient(name="Apple", gi=40.0)
        self.assertEqual(apple.gi, 40.0)

        # Check we can update it
        apple.gi = 50.0
        self.assertEqual(apple.gi, 50.0)

    def test_nutrient_quantities(self):
        """Check the nutrient quantities property gets and sets nutrient quantities correctly."""
        apple = Ingredient(name="Apple")

        # Check the nutrient quantities are empty to start
        self.assertEqual(len(apple.nutrient_quantities), 0)

        # Check we can add a nutrient quantity
        protein_quantity = self.nutrient_fixtures.create_ingredient_nutrient_quantity(
            "protein", apple
        )
        apple.add_nutrient_quantity(protein_quantity)
        self.assertEqual(len(apple.nutrient_quantities), 1)

    def test_get_flag_by_name(self):
        """Check we can retrieve a flag by its name."""
        apple = Ingredient(name="Apple")
        vegan_flag = self.flag_fixtures.create_ingredient_flag("vegan", apple)
        vegetarian_flag = self.flag_fixtures.create_ingredient_flag("vegetarian", apple)
        apple.add_flags([vegan_flag, vegetarian_flag])

        self.assertEqual(apple.get_flag_by_name("vegan"), vegan_flag)

    def test_remove_flag(self):
        """Check that we can remove a flag."""
        apple = Ingredient(name="Apple")
        vegan_flag = self.flag_fixtures.create_ingredient_flag("vegan", apple)
        vegetarian_flag = self.flag_fixtures.create_ingredient_flag("vegetarian", apple)
        apple.add_flags([vegan_flag, vegetarian_flag])

        # Check the flags are there
        self.assertEqual(len(apple.flags), 2)

        # Remove one
        apple.remove_flag(vegan_flag)

        # Check it is removed
        self.assertEqual(len(apple.flags), 1)
        self.assertNotIn(vegan_flag, apple.flags)

    def test_get_nutrient_quantity_by_name(self):
        """Check we can retrieve a nutrient quantity by its name."""
        apple = Ingredient(name="Apple")
        protein_quantity = self.nutrient_fixtures.create_ingredient_nutrient_quantity(
            "protein", apple
        )
        carb_quantity = self.nutrient_fixtures.create_ingredient_nutrient_quantity(
            "carbohydrate", apple
        )
        apple.add_nutrient_quantities([protein_quantity, carb_quantity])

        self.assertEqual(
            apple.get_nutrient_quantity_by_name("protein"), protein_quantity
        )

    def test_remove_nutrient_quantities(self):
        """Check that we can remove an ingredient nutrient quantity."""
        apple = Ingredient(name="Apple")
        protein_quantity = self.nutrient_fixtures.create_ingredient_nutrient_quantity(
            "protein", apple
        )
        apple.add_nutrient_quantity(protein_quantity)
        self.assertIn(protein_quantity, apple.nutrient_quantities)

        apple.remove_nutrient_quantity(protein_quantity)

        self.assertNotIn(protein_quantity, apple.nutrient_quantities)

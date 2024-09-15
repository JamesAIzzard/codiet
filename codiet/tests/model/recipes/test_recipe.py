"""Tests for the Recipe class."""

from unittest import TestCase

from codiet.model.recipes import Recipe
from codiet.model.time import TimeWindow
from codiet.model.tags import Tag
from codiet.tests.fixtures import IngredientTestFixtures, UnitTestFixtures

class TestRecipe(TestCase):
    """Test class for the Recipe class."""

    def setUp(self):
        self.unit_fixtures = UnitTestFixtures()
        self.ingredient_fixtures = IngredientTestFixtures(self.unit_fixtures)

    def test_constructor(self):
        """Checks that the recipe can be constructed and is an instance of the Recipe class."""
        recipe = Recipe(name="Apple Pie")
        self.assertIsInstance(recipe, Recipe)

    def test_name(self):
        """Check the name property returns correctly."""
        # Check we get the name we passed in the constructor
        recipe = Recipe(name="Apple Pie")
        self.assertEqual(recipe.name, "Apple Pie")

        # Check we can change the name
        recipe.name = "Apple Crumble"
        self.assertEqual(recipe.name, "Apple Crumble")

    def test_use_as_ingredient(self):
        """Check that the use_as_ingredient property sets and returns correctly."""
        # Check it is set correctly when passed in the constructor
        recipe = Recipe(name="Apple Pie")
        self.assertEqual(recipe.use_as_ingredient, False)

        # Check we can update it
        recipe.use_as_ingredient = True
        self.assertEqual(recipe.use_as_ingredient, True)

    def test_description(self):
        """Check that the description property sets and returns correctly."""
        # Check it is set correctly when passed in the constructor
        recipe = Recipe(name="Apple Pie", description="A delicious dessert")
        self.assertEqual(recipe.description, "A delicious dessert")

        # Check we can update it
        recipe.description = "A delicious dessert with pastry"
        self.assertEqual(recipe.description, "A delicious dessert with pastry")

    def test_instructions(self):
        """Check that the instructions property sets and returns correctly."""
        # Check it is set correctly when passed in the constructor
        recipe = Recipe(name="Apple Pie", instructions="Bake for 30 minutes")
        self.assertEqual(recipe.instructions, "Bake for 30 minutes")

        # Check we can update it
        recipe.instructions = "Bake for 40 minutes"
        self.assertEqual(recipe.instructions, "Bake for 40 minutes")

    def test_ingredient_quantities(self):
        """Check that the ingredient_quantities property sets and returns correctly."""
        # Check there are no ingredient quantities to start with
        recipe = Recipe(name="Apple Pie")
        self.assertEqual(len(recipe.ingredient_quantities), 0)

        # Add one and check it is added.
        apples = self.ingredient_fixtures.create_ingredient_quantity("apple")
        recipe.add_ingredient_quantity(apples)
        self.assertEqual(len(recipe.ingredient_quantities), 1)

    def test_serve_time_windows(self):
        """Check that the serve_time_windows property sets and returns correctly."""
        # Check there are no serve time windows to start with
        recipe = Recipe(name="Apple Pie")
        self.assertEqual(len(recipe.serve_time_windows), 0)

        # Add one and check it is added.
        window = TimeWindow()
        recipe.add_serve_time_window(window)
        self.assertEqual(len(recipe.serve_time_windows), 1)

    def test_tags(self):
        """Check that the tags property sets and returns correctly."""
        # Check there are no tags to start with
        recipe = Recipe(name="Apple Pie")
        self.assertEqual(len(recipe.tags), 0)

        # Add one and check it is added.
        recipe.add_tag(Tag("dessert"))
        self.assertEqual(len(recipe.tags), 1)
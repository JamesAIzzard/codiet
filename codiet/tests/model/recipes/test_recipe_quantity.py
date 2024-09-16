"""Defines tests for the RecipeQuantity class."""

from codiet.model.recipes import RecipeQuantity, Recipe
from codiet.tests.model import BaseModelTest


class BaseRecipeQuantityTest(BaseModelTest):
    """Base class for RecipeQuantity tests."""

    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseRecipeQuantityTest):
    """Test class for the RecipeQuantity class."""

    def test_minimal_arguments(self):
        """Checks that the recipe quantity can be constructed with only
        the recipe argument provided."""
        apple_pie = RecipeQuantity(Recipe("Apple Pie"))
        self.assertIsInstance(apple_pie, RecipeQuantity)
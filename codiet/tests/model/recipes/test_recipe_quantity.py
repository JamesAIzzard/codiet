"""Defines tests for the RecipeQuantity class."""

from codiet.model.recipes import RecipeQuantity, Recipe
from codiet.tests.model import BaseModelTest


class BaseRecipeQuantityTest(BaseModelTest):
    """Base class for RecipeQuantity tests."""

    def setUp(self) -> None:
        super().setUp()
        RecipeQuantity.setup(self._domain_service)

class TestConstructor(BaseRecipeQuantityTest):
    """Test class for the RecipeQuantity class."""

    def test_minimal_arguments(self):
        """Checks that the recipe quantity can be constructed with only
        the recipe argument provided."""
        apple_pie = RecipeQuantity(Recipe("Apple Pie"))
        self.assertIsInstance(apple_pie, RecipeQuantity)

    def test_unit_defaults_to_grams(self):
        """Checks that the quantity unit defaults to grams
        when not provided in the constructor."""
        apple_pie = RecipeQuantity(Recipe("Apple Pie"))
        self.assertIs(apple_pie.quantity_unit, self.unit_fixtures.gram)

    def test_quantity_defaults_to_none(self):
        """Checks that the quantity defaults to None when not provided in the constructor."""
        apple_pie = RecipeQuantity(Recipe("Apple Pie"))
        self.assertIsNone(apple_pie.quantity)

class TestQuantityUnitProperty(BaseRecipeQuantityTest):
    """Test class for the quantity_unit property."""

    def test_exception_raised_when_setting_to_none(self):
        """Checks that an exception is raised when setting the quantity unit to None."""
        apple_pie = RecipeQuantity(Recipe("Apple Pie"))
        with self.assertRaises(ValueError):
            apple_pie.quantity_unit = None # type: ignore
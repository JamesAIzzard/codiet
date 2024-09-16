"""Tests for the IngredientQuantity class."""

from codiet.tests.model import BaseModelTest
from codiet.tests.fixtures import IngredientTestFixtures
from codiet.model.ingredients import Ingredient, IngredientQuantity


class BaseIngredientQuantityTest(BaseModelTest):
    """Base class for testing IngredientQuantity elements."""

    def setUp(self) -> None:
        super().setUp()
        Ingredient.setup(self.domain_service)
        IngredientQuantity.setup(self.domain_service)
        self.ingredient_fixtures = IngredientTestFixtures()

class TestConstructor(BaseIngredientQuantityTest):

    def test_minimal_arguments(self):
        """Check that the ingredient quantity can be constructed with minimal arguments."""
        apple_quantity = IngredientQuantity(
            self.ingredient_fixtures.get_ingredient_by_name("apple")
        )
        self.assertIsInstance(apple_quantity, IngredientQuantity)

    def test_ingredient_is_set(self):
        """Check that the ingredient is set correctly."""
        apple = self.ingredient_fixtures.get_ingredient_by_name("apple")
        apple_quantity = IngredientQuantity(apple)
        self.assertIs(apple_quantity.ingredient, apple)

    def test_quantity_unit_is_default(self):
        """Check that the quantity unit is set to the default."""
        apple_quantity = IngredientQuantity(
            self.ingredient_fixtures.get_ingredient_by_name("apple")
        )
        self.assertIs(apple_quantity.quantity_unit, self.domain_service.gram)
        

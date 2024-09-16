"""Defines the test for the IsQuantity class."""

from codiet.model.quantity import is_quantity
from codiet.tests.model import BaseModelTest

class BaseIsQuantityTest(BaseModelTest):
    """Base class for testing the IsQuantity class."""
    
    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseIsQuantityTest):
    """Test class for the IsQuantity class."""

    def test_unit_defaults_to_grams(self):
        """Checks that the quantity unit defaults to grams when not provided in the constructor."""
        quantity = is_quantity.IsQuantity()
        self.assertIs(quantity.quantity_unit, self.unit_fixtures.gram)
    
    def test_quantity_value_defaults_to_none(self):
        """Checks that the quantity defaults to None when not provided in the constructor."""
        quantity = is_quantity.IsQuantity()
        self.assertIsNone(quantity.quantity_value)
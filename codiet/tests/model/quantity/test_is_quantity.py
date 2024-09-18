"""Defines tests for the IsQuantity class."""

from codiet.model.quantities import is_quantified
from codiet.tests.model import BaseModelTest

class BaseIsQuantityTest(BaseModelTest):
    """Base class for testing the IsQuantity class."""
    
    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseIsQuantityTest):
    """Test class for the IsQuantity class."""

    def test_unit_defaults_to_grams(self):
        """Checks that the quantity unit defaults to grams when not provided in the constructor."""
        test_quantity = is_quantified.IsQuantified()
        self.assertIs(test_quantity.quantity.unit, self.unit_fixtures.gram)
    
    def test_quantity_value_defaults_to_none(self):
        """Checks that the quantity defaults to None when not provided in the constructor."""
        test_quantity = is_quantified.IsQuantified()
        self.assertIsNone(test_quantity.quantity.value)
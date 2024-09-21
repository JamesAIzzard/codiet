from codiet.model.quantities import IsQuantified
from codiet.tests import BaseModelTest

class BaseIsQuantityTest(BaseModelTest):
    
    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseIsQuantityTest):

    def test_unit_defaults_to_grams(self):
        test_quantity = IsQuantified()
        self.assertIs(test_quantity.quantity.unit, self.quantities_fixtures.gram)
    
    def test_quantity_value_defaults_to_none(self):
        test_quantity = IsQuantified()
        self.assertIsNone(test_quantity.quantity.value)
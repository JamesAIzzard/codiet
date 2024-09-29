from codiet.model.quantities import IsQuantified, Quantity
from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.quantities import QuantitiesTestFixtures

class BaseIsQuantityTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()
        self.quantities_fixtures = self.fixture_manager.quantities_fixtures

class TestConstructor(BaseIsQuantityTest):

    def test_can_create_instance_without_args(self):
        is_quantified = IsQuantified()
        self.assertIsInstance(is_quantified, IsQuantified)

    def test_can_create_instance_with_args(self):
        is_quantified = IsQuantified(
            quantity=Quantity(
                value=100,
                unit=self.quantities_fixtures.get_unit("millilitre")
            )
        )
        self.assertIsInstance(is_quantified, IsQuantified)

    def test_quantity_is_set(self):
        quantity = Quantity(
            value=100,
            unit=self.quantities_fixtures.get_unit("millilitre")
        )
        is_quantified = IsQuantified(quantity=quantity)
        self.assertIs(is_quantified.quantity, quantity)
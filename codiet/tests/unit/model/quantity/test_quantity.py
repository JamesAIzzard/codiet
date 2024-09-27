from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.quantities import QuantitiesTestFixtures
from codiet.model.quantities import Quantity

class BaseQuantityTest(BaseCodietTest):
    def setUp(self) -> None:
        super().setUp()

        self.quantities_fixtures = QuantitiesTestFixtures.get_instance()

class TestConstructor(BaseQuantityTest):

    def test_minimal_arguments(self):
        quantity = Quantity()
        self.assertIsInstance(quantity, Quantity)

    def test_unit_defaults_to_grams(self):
        quantity = Quantity()
        self.assertEqual(quantity.unit, self.quantities_fixtures.gram)

class TestValueGetter(BaseQuantityTest):

    def test_can_get_value(self):
        quantity = Quantity.from_unit_name("gram").set_value(100)
        self.assertEqual(quantity.value, 100)

    def test_raises_error_if_value_not_set(self):
        quantity = Quantity()
        with self.assertRaises(TypeError):
            quantity.value
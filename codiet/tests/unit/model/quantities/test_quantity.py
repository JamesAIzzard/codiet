from codiet.tests import BaseCodietTest

class BaseQuantityTest(BaseCodietTest):
    pass

class TestUnit(BaseQuantityTest):
    
    def test_returns_unit(self):
        gram = self.singleton_register.get_unit("gram")

        quantity = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=1
        )

        self.assertEqual(quantity.unit, gram)

    def test_unit_is_immutable(self):
        quantity = self.quantities_factory.create_quantity(
            unit_name="gram", 
            value=100)
        with self.assertRaises(AttributeError):
            quantity.unit = self.singleton_register.get_unit("kilogram") # type: ignore

class TestIsDefined(BaseCodietTest): 

    def test_returns_true_if_defined(self):
        quantity = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=1
        )

        self.assertTrue(quantity.is_defined)
        
    def test_returns_false_if_not_defined(self):
        quantity = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=None
        )

        self.assertFalse(quantity.is_defined)

class TestEquality(BaseQuantityTest):
    
    def test_equal_quantities_considered_equal(self):
        quantity1 = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=1
        )
        quantity2 = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=1
        )

        self.assertEqual(quantity1, quantity2)

    def test_different_units_not_considered_equal(self):
        quantity1 = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=1
        )
        quantity2 = self.quantities_factory.create_quantity(
            unit_name="kilogram",
            value=1
        )

        self.assertNotEqual(quantity1, quantity2)

    def test_different_values_not_considered_equal(self):
        quantity1 = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=1
        )
        quantity2 = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=2
        )

        self.assertNotEqual(quantity1, quantity2)
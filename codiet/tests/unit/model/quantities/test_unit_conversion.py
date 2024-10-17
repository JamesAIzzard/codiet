from codiet.tests import BaseCodietTest
from codiet.model.quantities import Quantity

class BaseUnitConversionTest(BaseCodietTest):
    pass

class TestQuantities(BaseUnitConversionTest):
    
    def test_returns_quantity_instances(self):
        test_conversion = self.quantities_factory.create_unit_conversion(
            from_unit_name="gram",
            to_unit_name="kilogram",
            from_unit_quantity_value=1,
            to_unit_quantity_value=0.001
        )

        self.assertIsInstance(test_conversion.quantities["gram"], Quantity)
        self.assertIsInstance(test_conversion.quantities["kilogram"], Quantity)

    def test_quantity_value_is_immutable(self):
        test_conversion = self.quantities_factory.create_unit_conversion(
            from_unit_name="gram",
            to_unit_name="kilogram",
            from_unit_quantity_value=1,
            to_unit_quantity_value=0.001
        )

        with self.assertRaises(AttributeError):
            test_conversion.quantities["gram"].value = 2 # type: ignore
            test_conversion.quantities["kilogram"].value = 0.002 # type: ignore

class TestUnitNames(BaseUnitConversionTest):

    def test_returns_unit_names(self):
        test_conversion = self.quantities_factory.create_unit_conversion(
            from_unit_name="gram",
            to_unit_name="kilogram",
            from_unit_quantity_value=1,
            to_unit_quantity_value=0.001
        )

        self.assertEqual(test_conversion.unit_names, ("gram", "kilogram"))

class TestIsDefined(BaseUnitConversionTest):

    def test_returns_true_if_quantities_are_defined(self):
        test_conversion = self.quantities_factory.create_unit_conversion(
            from_unit_name="gram",
            to_unit_name="kilogram",
            from_unit_quantity_value=1,
            to_unit_quantity_value=0.001
        )

        self.assertTrue(test_conversion.is_defined)

    def test_returns_false_if_quantities_are_not_defined(self):
        grams_quantity = self.quantities_factory.create_quantity(
            unit_name="gram",
            value=None # type: ignore
        )
        litres_quantity = self.quantities_factory.create_quantity(
            unit_name="litre",
            value=10
        )
        test_conversion = self.quantities_factory.create_unit_conversion_from_quantities(
            from_quantity=grams_quantity,
            to_quantity=litres_quantity
        )

        self.assertFalse(test_conversion.is_defined)

class TestForwardsRatio(BaseUnitConversionTest):
    
        def test_returns_forwards_ratio(self):
            test_conversion = self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                to_unit_name="kilogram",
                from_unit_quantity_value=1,
                to_unit_quantity_value=0.001
            )
    
            self.assertEqual(test_conversion._forwards_ratio, 0.001)
    
        def test_raises_error_if_quantities_not_defined(self):
            grams_quantity = self.quantities_factory.create_quantity(
                unit_name="gram",
                value=None # type: ignore
            )
            litres_quantity = self.quantities_factory.create_quantity(
                unit_name="litre",
                value=10
            )
            test_conversion = self.quantities_factory.create_unit_conversion_from_quantities(
                from_quantity=grams_quantity,
                to_quantity=litres_quantity
            )
    
            with self.assertRaises(TypeError):
                test_conversion._forwards_ratio

class TestReverseRatio(BaseUnitConversionTest):
        
        def test_returns_reverse_ratio(self):
            test_conversion = self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                to_unit_name="kilogram",
                from_unit_quantity_value=1,
                to_unit_quantity_value=0.001
            )
    
            self.assertEqual(test_conversion._reverse_ratio, 1000)

class TestEquality(BaseUnitConversionTest):
         
        def test_returns_true_if_quantities_are_equal(self):
            test_conversion_1 = self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                to_unit_name="kilogram",
                from_unit_quantity_value=1,
                to_unit_quantity_value=0.001
            )
            test_conversion_2 = self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                to_unit_name="kilogram",
                from_unit_quantity_value=1,
                to_unit_quantity_value=0.001
            )
    
            self.assertEqual(test_conversion_1, test_conversion_2)
    
        def test_returns_false_if_quantities_are_not_equal(self):
            test_conversion_1 = self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                to_unit_name="kilogram",
                from_unit_quantity_value=1,
                to_unit_quantity_value=0.001
            )
            test_conversion_2 = self.quantities_factory.create_unit_conversion(
                from_unit_name="gram",
                to_unit_name="kilogram",
                from_unit_quantity_value=1,
                to_unit_quantity_value=0.002
            )
    
            self.assertNotEqual(test_conversion_1, test_conversion_2)
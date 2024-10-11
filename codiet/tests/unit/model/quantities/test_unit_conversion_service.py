from codiet.tests import BaseCodietTest
from codiet.model.quantities import ConversionUnavailableError

class BaseUnitConversionServiceTest(BaseCodietTest):
    pass

class TestGlobalUnitConversions(BaseUnitConversionServiceTest):
    def test_various_conversions_are_defined(self):
        self.assertIn(frozenset(["gram", "kilogram"]), self.unit_conversion_service.global_unit_conversions)
        self.assertIn(frozenset(["millilitre", "litre"]), self.unit_conversion_service.global_unit_conversions)

class TestGetAvailableUnitNames(BaseUnitConversionServiceTest):
    def test_gets_correct_units_from_starting_unit(self):
        available_units = self.unit_conversion_service.get_available_unit_names("gram")
        self.assertIn("kilogram", available_units)
        self.assertNotIn("litre", available_units)

        available_units = self.unit_conversion_service.get_available_unit_names("millilitre")
        self.assertIn("litre", available_units)
        self.assertNotIn("gram", available_units)

    def test_assumes_gram_if_starting_unit_not_specified(self):
        available_units = self.unit_conversion_service.get_available_unit_names()
        self.assertIn("kilogram", available_units)
        self.assertNotIn("litre", available_units)

class TestConvertQuantity(BaseUnitConversionServiceTest):
    def test_converts_quantity_using_global_conversions(self):
        grams_100 = self.quantities_factory.create_quantity("gram", 100)
        converted_qty = self.unit_conversion_service.convert_quantity(grams_100, "kilogram")
        self.assertEqual(converted_qty.unit.name, "kilogram")
        self.assertEqual(converted_qty.value, 0.1)

    def test_raises_error_if_no_conversion_available(self):
        grams_100 = self.quantities_factory.create_quantity("gram", 100)
        with self.assertRaises(ConversionUnavailableError):
            self.unit_conversion_service.convert_quantity(grams_100, "litre")

    def test_converts_mass_to_vol_when_given_appropriate_conversions(self):
        grams_100 = self.quantities_factory.create_quantity("gram", 100)
        gram_litre_conversion = self.quantities_factory.create_unit_conversion("gram", 1000, "litre", 1)
        
        converted_qty = self.unit_conversion_service.convert_quantity(
            quantity=grams_100, 
            to_unit_name="millilitre",
            instance_unit_conversons={frozenset(["gram", "litre"]): gram_litre_conversion}
        )
        
        self.assertEqual(converted_qty.unit.name, "millilitre")
        self.assertEqual(converted_qty.value, 100)
from codiet.tests import BaseCodietTest
from codiet.exceptions.quantities import UnitNotFoundError, UnitConversionNotFoundError

class BaseSingletonRegisterTest(BaseCodietTest):
    pass

class TestGetUnit(BaseSingletonRegisterTest):
    def test_gets_unit(self):
        unit = self.singleton_register.get_unit("gram")
        self.assertEqual(unit.name, "gram")

    def test_raises_error_if_unit_not_found(self):
        with self.assertRaises(UnitNotFoundError):
            self.singleton_register.get_unit("not_a_unit")

class TestGetGlobalUnitConversion(BaseSingletonRegisterTest):
    def test_gets_global_unit_conversion(self):
        unit_conversion = self.singleton_register.get_global_unit_conversion(frozenset(["gram", "kilogram"]))
        self.assertIn("gram", unit_conversion.unit_names)
        self.assertIn("kilogram", unit_conversion.unit_names)

    def test_raises_error_if_unit_conversion_not_found(self):
        with self.assertRaises(UnitConversionNotFoundError):
            self.singleton_register.get_global_unit_conversion(frozenset(["gram", "litre"]))


from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.quantities import QuantitiesTestFixtures
from codiet.model.quantities import UnitConversion, Quantity

class BaseUnitConversionTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()
        self.quantities_fixtures = self.fixture_manager.quantities_fixtures

class TestConstructor(BaseUnitConversionTest):

    def test_minimal_arguments(self) -> None:
        gram = self.quantities_fixtures.get_unit("gram")
        kilogram = self.quantities_fixtures.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram), Quantity(kilogram)))
        self.assertIsInstance(unit_conversion, UnitConversion)

    def test_exception_when_units_are_identical(self) -> None:
        gram = self.quantities_fixtures.get_unit("gram")
        with self.assertRaises(ValueError):
            UnitConversion((Quantity(gram), Quantity(gram)))

class TestIsDefined(BaseUnitConversionTest):
    
    def test_is_defined_returns_false_when_quantities_are_none(self) -> None:
        gram = self.quantities_fixtures.get_unit("gram")
        kilogram = self.quantities_fixtures.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram), Quantity(kilogram)))
        self.assertFalse(unit_conversion.is_defined)

    def test_is_defined_returns_true_when_quantities_are_not_none(self) -> None:
        gram = self.quantities_fixtures.get_unit("gram")
        kilogram = self.quantities_fixtures.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram, 1), Quantity(kilogram, 1000)))
        self.assertTrue(unit_conversion.is_defined)

class TestConvertFrom(BaseUnitConversionTest):
    
    def test_convert_from_raises_value_error_when_quantities_are_none(self) -> None:
        gram = self.quantities_fixtures.get_unit("gram")
        kilogram = self.quantities_fixtures.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram), Quantity(kilogram)))
        with self.assertRaises(ValueError):
            unit_conversion.convert_from(Quantity(gram))

    def test_convert_from_raises_value_error_when_unit_not_in_quantities(self) -> None:
        gram = self.quantities_fixtures.get_unit("gram")
        kilogram = self.quantities_fixtures.get_unit("kilogram")
        millilitre = self.quantities_fixtures.get_unit("millilitre")
        unit_conversion = UnitConversion((Quantity(gram, 1), Quantity(kilogram, 1000)))
        with self.assertRaises(ValueError):
            unit_conversion.convert_from(Quantity(millilitre, 1))

    def test_convert_from_forwards_returns_correct_quantity(self) -> None:
        gram = self.quantities_fixtures.get_unit("gram")
        kilogram = self.quantities_fixtures.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram, 1000), Quantity(kilogram, 1)))
        converted_quantity = unit_conversion.convert_from(Quantity(gram, 100))
        self.assertEqual(converted_quantity.value, 0.1)
        self.assertEqual(converted_quantity.unit, kilogram)

    def test_convert_from_reverse_returns_correct_quantity(self) -> None:
        gram = self.quantities_fixtures.get_unit("gram")
        kilogram = self.quantities_fixtures.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram, 1000), Quantity(kilogram, 1)))
        converted_quantity = unit_conversion.convert_from(Quantity(kilogram, 1))
        self.assertEqual(converted_quantity.value, 1000)
        self.assertEqual(converted_quantity.unit, gram)
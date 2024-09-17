"""This module contains unit tests for the UnitConversion class."""

from codiet.tests.model import BaseModelTest
from codiet.model.units import UnitConversion
from codiet.model.quantities import Quantity

class BaseUnitConversionTest(BaseModelTest):
    """Base class for testing the UnitConversion class."""
    
    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseUnitConversionTest):
    """Tests the constructor of the UnitConversion class."""

    def test_minimal_arguments(self) -> None:
        """Check that we can instantiate an instance with minimal arguments."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit_by_name("kilogram")
        unit_conversion = UnitConversion(Quantity(gram), Quantity(kilogram))
        self.assertIsInstance(unit_conversion, UnitConversion)

    def test_quantities_default_to_none(self) -> None:
        """Check that the quantities default to None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit_by_name("kilogram")
        unit_conversion = UnitConversion(gram, kilogram)
        self.assertIsNone(unit_conversion.from_unit_qty)
        self.assertIsNone(unit_conversion.to_unit_qty)

class TestIsDefined(BaseUnitConversionTest):
    """Tests the is_defined property of the UnitConversion class."""
    
    def test_is_defined_returns_false_when_quantities_are_none(self) -> None:
        """Check that is_defined returns False when the quantities are None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit_by_name("kilogram")
        unit_conversion = UnitConversion(gram, kilogram)
        self.assertFalse(unit_conversion.is_defined)

    def test_is_defined_returns_true_when_quantities_are_not_none(self) -> None:
        """Check that is_defined returns True when the quantities are not None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit_by_name("kilogram")
        unit_conversion = UnitConversion(gram, kilogram, 1, 1000)
        self.assertTrue(unit_conversion.is_defined)

class TestRatio(BaseUnitConversionTest):
    """Tests the ratio property of the UnitConversion class."""
    
    def test_ratio_raises_value_error_when_quantities_are_none(self) -> None:
        """Check that ratio raises a ValueError when the quantities are None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit_by_name("kilogram")
        unit_conversion = UnitConversion(gram, kilogram)
        with self.assertRaises(ValueError):
            unit_conversion.ratio

    def test_ratio_returns_correct_value(self) -> None:
        """Check that ratio returns the correct value."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit_by_name("kilogram")
        unit_conversion = UnitConversion(gram, kilogram, 1, 1000)
        self.assertEqual(unit_conversion.ratio, 1000)

class TestConvertQuantity(BaseUnitConversionTest):
    """Tests the convert_quantity method of the UnitConversion class."""
    
    def test_convert_quantity_raises_value_error_when_quantities_are_none(self) -> None:
        """Check that convert_quantity raises a ValueError when the quantities are None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit_by_name("kilogram")
        unit_conversion = UnitConversion(gram, kilogram)
        with self.assertRaises(ValueError):
            unit_conversion.convert(gram).to(kilogram).quantity(1)

    def test_convert_quantity_returns_correct_value(self) -> None:
        """Check that convert_quantity returns the correct value."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit_by_name("kilogram")
        unit_conversion = UnitConversion(gram, kilogram, 1, 1000)
        self.assertEqual(unit_conversion.convert_quantity(1), 1000)
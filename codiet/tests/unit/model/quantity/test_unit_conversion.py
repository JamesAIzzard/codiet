"""This module contains unit tests for the UnitConversion class."""

from codiet.tests import BaseCodietTest
from codiet.model.quantities import UnitConversion, Quantity

class BaseUnitConversionTest(BaseCodietTest):
    """Base class for testing the UnitConversion class."""
    
    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseUnitConversionTest):
    """Tests the constructor of the UnitConversion class."""

    def test_minimal_arguments(self) -> None:
        """Check that we can instantiate an instance with minimal arguments."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram), Quantity(kilogram)))
        self.assertIsInstance(unit_conversion, UnitConversion)

    def test_quantities_default_to_none(self) -> None:
        """Check that the quantities default to None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram), Quantity(kilogram)))
        for quantity in unit_conversion.quantities:
            self.assertIsNone(quantity.value)

class TestIsDefined(BaseUnitConversionTest):
    """Tests the is_defined property of the UnitConversion class."""
    
    def test_is_defined_returns_false_when_quantities_are_none(self) -> None:
        """Check that is_defined returns False when the quantities are None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram), Quantity(kilogram)))
        self.assertFalse(unit_conversion.is_defined)

    def test_is_defined_returns_true_when_quantities_are_not_none(self) -> None:
        """Check that is_defined returns True when the quantities are not None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram, 1), Quantity(kilogram, 1000)))
        self.assertTrue(unit_conversion.is_defined)

class TestForwardsRatio(BaseUnitConversionTest):
    """Tests the _forwards_ratio property of the UnitConversion class."""
    
    def test_forwards_ratio_raises_value_error_when_quantities_are_none(self) -> None:
        """Check that _forwards_ratio raises a ValueError when the quantities are None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram), Quantity(kilogram)))
        with self.assertRaises(ValueError):
            unit_conversion._forwards_ratio

    def test_forwards_ratio_returns_correct_value(self) -> None:
        """Check that _forwards_ratio returns the correct value."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram, 1), Quantity(kilogram, 1000)))
        self.assertEqual(unit_conversion._forwards_ratio, 1000)

class TestReverseRatio(BaseUnitConversionTest):
    """Tests the _reverse_ratio property of the UnitConversion class."""
    
    def test_reverse_ratio_raises_value_error_when_quantities_are_none(self) -> None:
        """Check that _reverse_ratio raises a ValueError when the quantities are None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram), Quantity(kilogram)))
        with self.assertRaises(ValueError):
            unit_conversion._reverse_ratio

    def test_reverse_ratio_returns_correct_value(self) -> None:
        """Check that _reverse_ratio returns the correct value."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram, 1), Quantity(kilogram, 1000)))
        self.assertEqual(unit_conversion._reverse_ratio, 0.001)

class TestConvertFrom(BaseUnitConversionTest):
    """Tests the convert_from method of the UnitConversion class."""
    
    def test_convert_from_raises_value_error_when_quantities_are_none(self) -> None:
        """Check that convert_from raises a ValueError when the quantities are None."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram), Quantity(kilogram)))
        with self.assertRaises(ValueError):
            unit_conversion.convert_from(Quantity(gram))

    def test_convert_from_raises_value_error_when_unit_not_in_quantities(self) -> None:
        """Check that convert_from raises a ValueError when the unit is not in the quantities."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        millilitre = self.domain_service.get_unit("millilitre")
        unit_conversion = UnitConversion((Quantity(gram, 1), Quantity(kilogram, 1000)))
        with self.assertRaises(ValueError):
            unit_conversion.convert_from(Quantity(millilitre, 1))

    def test_convert_from_forwards_returns_correct_quantity(self) -> None:
        """Check that convert_from returns the correct quantity."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram, 1000), Quantity(kilogram, 1)))
        converted_quantity = unit_conversion.convert_from(Quantity(gram, 100))
        self.assertEqual(converted_quantity.value, 0.1)
        self.assertEqual(converted_quantity.unit, kilogram)

    def test_convert_from_reverse_returns_correct_quantity(self) -> None:
        """Check that convert_from returns the correct quantity."""
        gram = self.domain_service.gram
        kilogram = self.domain_service.get_unit("kilogram")
        unit_conversion = UnitConversion((Quantity(gram, 1000), Quantity(kilogram, 1)))
        converted_quantity = unit_conversion.convert_from(Quantity(kilogram, 1))
        self.assertEqual(converted_quantity.value, 1000)
        self.assertEqual(converted_quantity.unit, gram)
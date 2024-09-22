"""This module contains the unit tests for the Unit class."""

from codiet.tests import BaseCodietTest
from codiet.model.quantities.unit import Unit

class BaseUnitTest(BaseCodietTest):
    """Base class for testing the Unit class."""
    
    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseUnitTest):
    def test_minimal_arguments(self):
        unit = Unit("gram", "mass")
        self.assertIsInstance(unit, Unit)
    
    def test_default_abbreviations(self):
        unit = Unit("gram", "mass")
        self.assertEqual(unit.singular_abbreviation, "gram")
        self.assertEqual(unit.plural_abbreviation, "gram")

    def test_constructor_with_abbreviations(self):
        unit = Unit("gram", "mass", "g", "g")
        self.assertEqual(unit.singular_abbreviation, "g")
        self.assertEqual(unit.plural_abbreviation, "g")
"""Defines the tests for the UnitSystem class."""

from codiet.tests.model import BaseModelTest
from codiet.tests.fixtures import UnitTestFixtures
from codiet.model.quantities import UnitSystem, UnitConversion, Quantity

class BaseUnitSystemTest(BaseModelTest):
    """Base class for testing the UnitSystem class."""
    
    def setUp(self) -> None:
        super().setUp()
        self.unit_fixtures = UnitTestFixtures()

class TestConstructor(BaseUnitSystemTest):
    def test_minimal_arguments(self):
        """Check we can construct a UnitSystem object with no arguments."""
        unit_system = UnitSystem()
        self.assertIsInstance(unit_system, UnitSystem)
        self.assertEqual(len(unit_system.entity_unit_conversions), 0)

    def test_with_entity_unit_conversions(self):
        """Check we can construct a UnitSystem object with entity unit conversions."""
        gram_millilitre = UnitConversion(
            (
                Quantity(self.unit_fixtures.get_unit_by_name("gram"), 1),
                Quantity(self.unit_fixtures.get_unit_by_name("millilitre"), 1)
            )
        )
        unit_system = UnitSystem([gram_millilitre])
        self.assertIsInstance(unit_system, UnitSystem)
        self.assertEqual(len(unit_system.entity_unit_conversions), 1)
    
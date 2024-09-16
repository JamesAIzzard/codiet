"""Defines the base class test for testing model elements."""

from unittest import TestCase

from codiet.model.domain_service import DomainService
from codiet.tests.fixtures import (
    UnitTestFixtures,
    FlagTestFixtures,
    NutrientTestFixtures,
    IngredientTestFixtures
)


class BaseModelTest(TestCase):
    """Base class for testing model elements."""

    def setUp(self) -> None:
        self.unit_fixtures = UnitTestFixtures()
        self.flag_fixtures = FlagTestFixtures()
        self.nutrient_fixtures = NutrientTestFixtures()

        self.domain_service = DomainService(
            global_units=self.unit_fixtures.units.values(),
            global_unit_conversions=self.unit_fixtures.global_unit_conversions.values(),
            global_flags=self.flag_fixtures.flags.values(),
            global_nutrients=self.nutrient_fixtures.nutrients.values(),
        )

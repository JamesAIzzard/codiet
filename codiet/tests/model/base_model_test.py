"""Defines the base class test for testing model elements."""

from unittest import TestCase

from codiet.model.domain_service import DomainService
from codiet.tests.fixtures import (
    UnitTestFixtures,
    FlagTestFixtures,
    NutrientTestFixtures
)


class BaseModelTest(TestCase):
    """Base class for testing model elements."""

    @property
    def domain_service(self) -> DomainService:
        """Returns the domain service."""
        return self._domain_service

    def setUp(self) -> None:
        """Intialises a domain service, which is required by various model classes
        to access global units, unit conversions, flags, and nutrients.
        """
        self._init_essential_fixtures()
        self._init_domain_service()

        self._domain_service = DomainService.get_instance()

    def _init_essential_fixtures(self):
        """Initialises the global fixtures required for testing."""
        self.unit_fixtures = UnitTestFixtures()
        self.flag_fixtures = FlagTestFixtures()
        self.nutrient_fixtures = NutrientTestFixtures()

    def _init_domain_service(self):
        """Builds a domain service with the test fixtures."""
        DomainService(
            global_units=self.unit_fixtures.units.values(),
            global_unit_conversions=self.unit_fixtures.global_unit_conversions.values(),
            global_flags=self.flag_fixtures.flags.values(),
            global_nutrients=self.nutrient_fixtures.nutrients.values(),
        )

"""Defines the base class test for testing model elements."""

from unittest import TestCase

from codiet.model import DomainService
from codiet.tests.fixtures import UnitTestFixtures

class BaseModelTest(TestCase):
    """Base class for testing model elements."""

    def setUp(self) -> None:
        self.unit_fixtures = UnitTestFixtures()
        self.domain_service = DomainService(
            global_units=self.unit_fixtures.units.values(),
            global_unit_conversions=self.unit_fixtures.global_unit_conversions.values(),
        )
        
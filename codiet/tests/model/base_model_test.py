from codiet.model.domain_service import DomainService
from codiet.tests import BaseCodietTest
from codiet.tests.fixtures import (
    UnitTestFixtures,
    FlagTestFixtures,
    NutrientTestFixtures
)


class BaseModelTest(BaseCodietTest):
    """Base class for testing model elements."""

    @property
    def domain_service(self) -> DomainService:
        return self._domain_service

    def setUp(self) -> None:
        super().setUp()
        self._init_essential_fixtures()
        self._init_domain_service()

        self._domain_service = DomainService.get_instance()

    def tearDown(self) -> None:
        return super().tearDown()


    def _init_essential_fixtures(self):
        self.unit_fixtures = UnitTestFixtures()
        self.flag_fixtures = FlagTestFixtures()
        self.nutrient_fixtures = NutrientTestFixtures()

    def _init_domain_service(self):
        DomainService(
            global_units=self.unit_fixtures.units.values(),
            global_unit_conversions=self.unit_fixtures.global_unit_conversions.values(),
            global_flags=self.flag_fixtures.flags.values(),
            global_nutrients=self.nutrient_fixtures.nutrients.values(),
        )

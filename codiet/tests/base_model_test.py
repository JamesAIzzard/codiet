from codiet.model.domain_service import DomainService
from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.nutrients import NutrientTestFixtures
from codiet.tests.fixtures.quantities import QuantitiesTestFixtures
from codiet.tests.fixtures.flags import FlagTestFixtures


class BaseModelTest(BaseCodietTest):

    @property
    def domain_service(self) -> DomainService:
        return self._domain_service

    def setUp(self) -> None:
        super().setUp()
        
        self._init_essential_fixtures()
        self._init_domain_service()

        self._domain_service = DomainService.get_instance()

    def _init_essential_fixtures(self):
        self.quantities_fixtures = QuantitiesTestFixtures()
        self.flag_fixtures = FlagTestFixtures()
        self.nutrient_fixtures = NutrientTestFixtures()

    def _init_domain_service(self):
        DomainService.initialise(
            units=self.quantities_fixtures.units,
            global_unit_conversions=self.quantities_fixtures.global_unit_conversions,
            flag_definitions=self.flag_fixtures.flag_definitions,
            nutrients=self.nutrient_fixtures.nutrients
        )

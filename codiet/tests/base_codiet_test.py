from unittest import TestCase

from codiet.utils.singleton import SingletonInitError
from codiet.model.domain_service import DomainService
from codiet.tests.fixtures.flags.flag_test_fixtures import FlagTestFixtures
from codiet.tests.fixtures.ingredients.ingredient_test_fixtures import IngredientTestFixtures
from codiet.tests.fixtures.nutrients.nutrient_test_fixtures import NutrientTestFixtures
from codiet.tests.fixtures.quantities.quantities_test_fixtures import QuantitiesTestFixtures
from codiet.tests.fixtures.recipes.recipe_test_fixtures import RecipeTestFixtures
from codiet.tests.fixtures.time.time_test_fixtures import TimeTestFixtures


class BaseCodietTest(TestCase):

    @property
    def domain_service(self) -> DomainService:
        return DomainService.get_instance()     
    
    @property
    def flag_fixtures(self) -> 'FlagTestFixtures':
        return self._get_or_initialize_fixture(FlagTestFixtures)
    
    @property
    def ingredient_fixtures(self) -> 'IngredientTestFixtures':
        return self._get_or_initialize_fixture(IngredientTestFixtures)
    
    @property
    def nutrient_fixtures(self) -> 'NutrientTestFixtures':
        return self._get_or_initialize_fixture(NutrientTestFixtures)

    @property
    def quantities_fixtures(self) -> 'QuantitiesTestFixtures':
        return self._get_or_initialize_fixture(QuantitiesTestFixtures)
    
    @property
    def recipe_fixtures(self) -> 'RecipeTestFixtures':
        return self._get_or_initialize_fixture(RecipeTestFixtures)
    
    @property
    def time_fixtures(self) -> 'TimeTestFixtures':
        return self._get_or_initialize_fixture(TimeTestFixtures)
    
    def _get_or_initialize_fixture(self, fixture_class):
        try:
            return fixture_class.get_instance()
        except SingletonInitError:
            fixture_class.initialise()
            return fixture_class.get_instance()

    def setUp(self) -> None:
        super().setUp()

        self.reset_fixtures()

        self.reset_domain_service()
        # Domain service must be initialized in setUp because
        # model classes use it, and so lazy init in this class
        # might be too late.
        DomainService.initialise(
            units=self.quantities_fixtures.units,
            global_unit_conversions=self.quantities_fixtures.global_unit_conversions,
            flag_definitions=self.flag_fixtures.flag_definitions,
            nutrients=self.nutrient_fixtures.nutrients
        )

    def reset_fixtures(self) -> None:
        FlagTestFixtures.clear_instance()
        IngredientTestFixtures.clear_instance()
        NutrientTestFixtures.clear_instance()
        QuantitiesTestFixtures.clear_instance()
        RecipeTestFixtures.clear_instance()
        TimeTestFixtures.clear_instance()

    def reset_domain_service(self) -> None:
        DomainService.clear_instance()

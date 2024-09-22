from typing import TYPE_CHECKING

from unittest import TestCase

from codiet.model.domain_service import DomainService
from codiet.tests.fixtures import Fixtures

if TYPE_CHECKING:
    from codiet.tests.fixtures.flags.flag_test_fixtures import FlagTestFixtures
    from codiet.tests.fixtures.ingredients.ingredient_test_fixtures import IngredientTestFixtures
    from codiet.tests.fixtures.nutrients.nutrient_test_fixtures import NutrientTestFixtures
    from codiet.tests.fixtures.quantities.quantities_test_fixtures import QuantitiesTestFixtures
    from codiet.tests.fixtures.recipes.recipe_test_fixtures import RecipeTestFixtures
    from codiet.tests.fixtures.time.time_test_fixtures import TimeTestFixtures


class BaseModelTest(TestCase):

    def setUp(self) -> None:
        super().setUp()

        Fixtures.initialise()
        self._fixtures = Fixtures.get_instance()

        DomainService.initialise(
            units=self._fixtures.units,
            global_unit_conversions=self._fixtures.global_unit_conversions,
            flag_definitions=self._fixtures.flag_definitions,
            nutrients=self._fixtures.nutrients
        )
        self._domain_service = DomainService.get_instance()

    @property
    def domain_service(self) -> DomainService:
        return self._domain_service
    
    @property
    def flag_fixtures(self) -> 'FlagTestFixtures':
        return self._fixtures.flag_fixtures
    
    @property
    def ingredient_fixtures(self) -> 'IngredientTestFixtures':
        return self._fixtures.ingredient_fixtures
    
    @property
    def nutrient_fixtures(self) -> 'NutrientTestFixtures':
        return self._fixtures.nutrient_fixtures

    @property
    def quantities_fixtures(self) -> 'QuantitiesTestFixtures':
        return self._fixtures.quantities_fixtures
    
    @property
    def recipe_fixtures(self) -> 'RecipeTestFixtures':
        return self._fixtures.recipe_fixtures
    
    @property
    def time_fixtures(self) -> 'TimeTestFixtures':
        return self._fixtures.time_fixtures
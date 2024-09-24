from unittest import TestCase

from codiet.model.domain_service import DomainService
from codiet.tests.fixtures.flags.flag_test_fixtures import FlagTestFixtures
from codiet.tests.fixtures.ingredients.ingredient_test_fixtures import IngredientTestFixtures
from codiet.tests.fixtures.nutrients.nutrient_test_fixtures import NutrientTestFixtures
from codiet.tests.fixtures.quantities.quantities_test_fixtures import QuantitiesTestFixtures
from codiet.tests.fixtures.recipes.recipe_test_fixtures import RecipeTestFixtures
from codiet.tests.fixtures.time.time_test_fixtures import TimeTestFixtures
from codiet.tests.fixtures.constraints import ConstraintTestFixtures
from codiet.tests.fixtures.optimiser import OptimiserTestFixtures


class BaseCodietTest(TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._fixtures = [
            FlagTestFixtures,
            IngredientTestFixtures,
            NutrientTestFixtures,
            QuantitiesTestFixtures,
            RecipeTestFixtures,
            TimeTestFixtures,
            ConstraintTestFixtures,
            OptimiserTestFixtures
        ]

    def setUp(self) -> None:
        super().setUp()

        # Since modules which do not subclass this class have access to these singletons,
        # we can't lazy initialise them in the properties here.
        self.reset_fixtures()
        self.initialise_fixtures()

        self.reset_domain_service()

        quantities_fixtures = QuantitiesTestFixtures.get_instance()
        flag_fixtures = FlagTestFixtures.get_instance()
        nutrient_fixtures = NutrientTestFixtures.get_instance()

        DomainService.initialise(
            units=quantities_fixtures.units,
            global_unit_conversions=quantities_fixtures.global_unit_conversions,
            flag_definitions=flag_fixtures.flag_definitions,
            nutrients=nutrient_fixtures.nutrients
        )

    def reset_fixtures(self) -> None:
        for fixture in self._fixtures:
            fixture.clear_instance()

    def initialise_fixtures(self) -> None:
        for fixture in self._fixtures:
            fixture.initialise()

    def reset_domain_service(self) -> None:
        DomainService.clear_instance()

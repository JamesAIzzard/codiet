from unittest import TestCase

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
    def flag_fixtures(self) -> FlagTestFixtures:
        return FlagTestFixtures.get_instance()
    
    @property
    def ingredient_fixtures(self) -> IngredientTestFixtures:
        return IngredientTestFixtures.get_instance()
    
    @property
    def nutrient_fixtures(self) -> NutrientTestFixtures:
        return NutrientTestFixtures.get_instance()

    @property
    def quantities_fixtures(self) -> QuantitiesTestFixtures:
        return QuantitiesTestFixtures.get_instance()
    
    @property
    def recipe_fixtures(self) -> RecipeTestFixtures:
        return RecipeTestFixtures.get_instance()
    
    @property
    def time_fixtures(self) -> TimeTestFixtures:
        return TimeTestFixtures.get_instance()

    def setUp(self) -> None:
        super().setUp()

        # Since modules which do not subclass this class have access to these singletons,
        # we can't lazy initialise them in the properties here.
        self.reset_fixtures()
        self.initialise_fixtures()

        self.reset_domain_service()
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

    def initialise_fixtures(self) -> None:
        FlagTestFixtures.initialise()
        IngredientTestFixtures.initialise()
        NutrientTestFixtures.initialise()
        QuantitiesTestFixtures.initialise()
        RecipeTestFixtures.initialise()
        TimeTestFixtures.initialise()

    def reset_domain_service(self) -> None:
        DomainService.clear_instance()

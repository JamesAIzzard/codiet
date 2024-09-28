from typing import Any, Type

from codiet.tests.fixtures.flags.flag_test_fixtures import FlagTestFixtures
from codiet.tests.fixtures.ingredients.ingredient_test_fixtures import IngredientTestFixtures
from codiet.tests.fixtures.nutrients.nutrient_test_fixtures import NutrientTestFixtures
from codiet.tests.fixtures.quantities.quantities_test_fixtures import QuantitiesTestFixtures
from codiet.tests.fixtures.recipes.recipe_test_fixtures import RecipeTestFixtures
from codiet.tests.fixtures.time.time_test_fixtures import TimeTestFixtures
from codiet.tests.fixtures.constraints import ConstraintTestFixtures
from codiet.tests.fixtures.optimiser import OptimiserTestFixtures

class FixtureManager:
    def __init__(self):
        self._fixtures: dict[str, Any] = {
            'flag_fixtures': None,
            'ingredient_fixtures': None,
            'nutrient_fixtures': None,
            'quantities_fixtures': None,
            'recipe_fixtures': None,
            'time_fixtures': None,
            'constraint_fixtures': None,
            'optimiser_fixtures': None
        }

    def _get_fixture(self, name: str, cls: Type[Any]) -> Any:
        if self._fixtures[name] is None:
            self._fixtures[name] = cls._create_instance()
        return self._fixtures[name]

    @property
    def flag_fixtures(self) -> FlagTestFixtures:
        return self._get_fixture('flag_fixtures', FlagTestFixtures)

    @property
    def ingredient_fixtures(self) -> IngredientTestFixtures:
        return self._get_fixture('ingredient_fixtures', IngredientTestFixtures)

    @property
    def nutrient_fixtures(self) -> NutrientTestFixtures:
        return self._get_fixture('nutrient_fixtures', NutrientTestFixtures)

    @property
    def quantities_fixtures(self) -> QuantitiesTestFixtures:
        return self._get_fixture('quantities_fixtures', QuantitiesTestFixtures)

    @property
    def recipe_fixtures(self) -> RecipeTestFixtures:
        return self._get_fixture('recipe_fixtures', RecipeTestFixtures)

    @property
    def time_fixtures(self) -> TimeTestFixtures:
        return self._get_fixture('time_fixtures', TimeTestFixtures)

    @property
    def constraint_fixtures(self) -> ConstraintTestFixtures:
        return self._get_fixture('constraint_fixtures', ConstraintTestFixtures)

    @property
    def optimiser_fixtures(self) -> OptimiserTestFixtures:
        return self._get_fixture('optimiser_fixtures', OptimiserTestFixtures)
    
    def reset_fixtures(self) -> None:
        for key in self._fixtures:
            self._fixtures[key] = None
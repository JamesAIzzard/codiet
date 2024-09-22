from typing import TYPE_CHECKING, Callable

from codiet.utils import SingletonMeta
from .flags.flag_test_fixtures import FlagTestFixtures
from .ingredients.ingredient_test_fixtures import IngredientTestFixtures
from .nutrients.nutrient_test_fixtures import NutrientTestFixtures
from .quantities.quantities_test_fixtures import QuantitiesTestFixtures
from .recipes.recipe_test_fixtures import RecipeTestFixtures
from .time.time_test_fixtures import TimeTestFixtures

if TYPE_CHECKING:
    from codiet.model.flags import FlagDefinition
    from codiet.model.quantities import Quantity, Unit, UnitConversion
    from codiet.model.nutrients import Nutrient
    from codiet.model.ingredients import IngredientQuantity

class Fixtures(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self._flag_test_fixtures: FlagTestFixtures|None = None
        self._nutrient_test_fixtures: NutrientTestFixtures|None = None
        self._quantities_test_fixtures: QuantitiesTestFixtures|None = None
        self._recipe_test_fixtures: RecipeTestFixtures|None = None
        self._ingredient_test_fixtures: IngredientTestFixtures|None = None
        self._time_test_fixtures: TimeTestFixtures|None = None

    @property
    def flag_fixtures(self) -> FlagTestFixtures:
        if self._flag_test_fixtures is None:
            self._flag_test_fixtures = FlagTestFixtures()
        return self._flag_test_fixtures
    
    @property
    def flag_definitions(self) -> dict[str, 'FlagDefinition']:
        return self.flag_fixtures.flag_definitions

    @property
    def nutrient_fixtures(self) -> NutrientTestFixtures:
        if self._nutrient_test_fixtures is None:
            self._nutrient_test_fixtures = NutrientTestFixtures()
        return self._nutrient_test_fixtures
    
    @property
    def nutrients(self) -> dict[str, 'Nutrient']:
        return self.nutrient_fixtures.nutrients

    @property
    def quantities_fixtures(self) -> QuantitiesTestFixtures:
        if self._quantities_test_fixtures is None:
            self._quantities_test_fixtures = QuantitiesTestFixtures()
        return self._quantities_test_fixtures
    
    @property
    def units(self) -> dict[str, 'Unit']:
        return self.quantities_fixtures.units

    @property
    def global_unit_conversions(self) -> dict[tuple[str, str], 'UnitConversion']:
        return self.quantities_fixtures.global_unit_conversions

    @property
    def recipe_fixtures(self) -> RecipeTestFixtures:
        if self._recipe_test_fixtures is None:
            self._recipe_test_fixtures = RecipeTestFixtures()
        return self._recipe_test_fixtures
    
    @property
    def ingredient_fixtures(self) -> IngredientTestFixtures:
        if self._ingredient_test_fixtures is None:
            self._ingredient_test_fixtures = IngredientTestFixtures()
        return self._ingredient_test_fixtures

    @property
    def create_ingredient_quantity(self) -> Callable[[str, 'Quantity'], 'IngredientQuantity']:
        return self.ingredient_fixtures.create_ingredient_quantity

    @property
    def time_fixtures(self) -> TimeTestFixtures:
        if self._time_test_fixtures is None:
            self._time_test_fixtures = TimeTestFixtures()
        return self._time_test_fixtures
    

    def reset(self) -> None:
        self._flag_test_fixtures = None
        self._nutrient_test_fixtures = None
        self._quantities_test_fixtures = None
        self._recipe_test_fixtures = None
        self._ingredient_test_fixtures = None
        self._time_test_fixtures = None    
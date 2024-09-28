from unittest import TestCase

from codiet.tests.fixtures import FixtureManager
from codiet.model import SingletonRegistry

class BaseCodietTest(TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._fixture_manager:FixtureManager|None = None

    def setUp(self) -> None:
        super().setUp()
        self._reset_fixture_manager()
        self._reset_singleton_registry()

    @property
    def fixture_manager(self) -> FixtureManager:
        if self._fixture_manager is None:
            self._fixture_manager = FixtureManager()
        return self._fixture_manager

    def _reset_fixture_manager(self):
        self._fixture_manager = None

    def _reset_singleton_registry(self):
        singleton_registry = SingletonRegistry()
        singleton_registry.set_unit_loader(
            self.fixture_manager.quantities_fixtures.get_unit
        )
        singleton_registry.set_global_unit_conversion_loader(
            self.fixture_manager.quantities_fixtures.get_global_unit_conversion,
        )
        singleton_registry.set_flag_loader(
            self.fixture_manager.flag_fixtures.get_flag_definition
        )
        singleton_registry.set_nutrient_loader(
            self.fixture_manager.nutrient_fixtures.get_nutrient
        )
        singleton_registry.set_recipe_loader(
            self.fixture_manager.recipe_fixtures.get_recipe
        )
        singleton_registry.set_ingredient_loader(
            self.fixture_manager.ingredient_fixtures.get_ingredient
        )



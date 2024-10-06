import os
from unittest import TestCase

from .fixtures import OptimiserFixtures
from codiet.data import DatabaseService, JSONRepository
from codiet.model import SingletonRegister
from codiet.model.quantities import QuantitiesFactory
from codiet.model.cost import CostFactory
from codiet.model.flags import FlagFactory
from codiet.model.nutrients import NutrientFactory
from codiet.model.tags import TagFactory
from codiet.model.ingredients import IngredientFactory
from codiet.model.recipes import RecipeFactory

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(CURRENT_DIR, "json_data")

class BaseCodietTest(TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.database_service = DatabaseService()
        repository = JSONRepository(TEST_DATA_DIR)
        self.database_service._repository = repository

        self.singleton_register = SingletonRegister()

        self.quantities_factory = QuantitiesFactory()
        self.cost_factory = CostFactory()
        self.flag_factory = FlagFactory()
        self.nutrient_factory = NutrientFactory()
        self.tag_factory = TagFactory()
        self.ingredient_factory = IngredientFactory()
        self.recipe_factory = RecipeFactory()

        self.database_service._quantities_factory = self.quantities_factory
        self.database_service._nutrients_factory = self.nutrient_factory
        self.database_service._ingredient_factory = self.ingredient_factory
        self.database_service._recipe_factory = self.recipe_factory

        self.singleton_register._database_service = self.database_service
        self.singleton_register._tag_factory = self.tag_factory

        self.quantities_factory._singleton_register = self.singleton_register

        self.cost_factory._quantities_factory = self.quantities_factory

        self.nutrient_factory._singleton_register = self.singleton_register

        self.ingredient_factory._singleton_register = self.singleton_register
        self.ingredient_factory._quantities_factory = self.quantities_factory
        self.ingredient_factory._cost_factory = self.cost_factory
        self.ingredient_factory._flag_factory = self.flag_factory
        self.ingredient_factory._nutrients_factory = self.nutrient_factory

        self.recipe_factory._singleton_register = self.singleton_register
        self.recipe_factory._ingredient_factory = self.ingredient_factory

        self.optimiser_fixtures = OptimiserFixtures()



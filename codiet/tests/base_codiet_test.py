import os
from unittest import TestCase

from .fixtures import OptimiserFixtures, RecipeFixtures
from codiet.data import DatabaseService, JSONRepository
from codiet.model import SingletonRegister
from codiet.model.quantities import QuantitiesFactory, UnitConversionService
from codiet.model.cost import CostFactory
from codiet.model.flags import FlagFactory
from codiet.model.nutrients import NutrientFactory
from codiet.model.tags import TagFactory
from codiet.model.time import TimeFactory
from codiet.model.ingredients import IngredientFactory
from codiet.model.recipes import RecipeFactory
from codiet.optimisation import OptimiserFactory

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(CURRENT_DIR, "json_data")

class BaseCodietTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.database_service = DatabaseService()
        self.json_repository = JSONRepository(TEST_DATA_DIR)        
        
        self.singleton_register = SingletonRegister()
        self.unit_conversion_service = UnitConversionService()

        self.quantities_factory = QuantitiesFactory()
        self.cost_factory = CostFactory()
        self.flag_factory = FlagFactory()
        self.nutrient_factory = NutrientFactory()
        self.tag_factory = TagFactory()
        self.time_factory = TimeFactory()
        self.ingredient_factory = IngredientFactory()
        self.recipe_factory = RecipeFactory()
        self.optimiser_factory = OptimiserFactory()

        self.optimiser_fixtures = OptimiserFixtures()
        self.recipe_fixtures = RecipeFixtures()

        self.database_service.initialise(
            repository=self.json_repository,
            quantities_factory=self.quantities_factory,
            nutrients_factory=self.nutrient_factory,
            ingredient_factory=self.ingredient_factory,
            recipe_factory=self.recipe_factory
        )

        self.singleton_register.initialise(
            database_service=self.database_service,
            quantities_factory=self.quantities_factory,
            tag_factory=self.tag_factory
        )

        self.unit_conversion_service.initialise(
            create_quantity=self.quantities_factory.create_quantity,
            get_unit=self.singleton_register.get_unit,
            get_global_unit_conversions=self.singleton_register.get_global_unit_conversions
        )

        self.quantities_factory.initialise(
            singleton_register=self.singleton_register,
            database_service=self.database_service
        )

        self.cost_factory.initialise(
            quantities_factory=self.quantities_factory
        )

        self.nutrient_factory.initialise(
            singleton_register=self.singleton_register,
            quantities_factory=self.quantities_factory
        )

        self.ingredient_factory.initialise(
            singleton_register=self.singleton_register,
            quantities_factory=self.quantities_factory,
            cost_factory=self.cost_factory,
            flag_factory=self.flag_factory,
            nutrient_factory=self.nutrient_factory
        )

        self.recipe_factory.initialise(
            singleton_register=self.singleton_register,
            unit_conversion_service=self.unit_conversion_service,
            quantities_factory=self.quantities_factory,
            time_factory=self.time_factory,
            flag_factory=self.flag_factory,
            ingredient_factory=self.ingredient_factory
        )

        self.optimiser_factory.initialise(
            recipe_factory=self.recipe_factory
        )

        self.recipe_fixtures.initialise(
            recipe_factory=self.recipe_factory,
        )

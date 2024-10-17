import os
from unittest import TestCase

from .fixtures import OptimiserFixtures, RecipeFixtures
from codiet.data import DatabaseService, JSONRepository
from codiet.model import SingletonRegister
from codiet.model.quantities import QuantitiesFactory, UnitConversionService
from codiet.model.cost import CostFactory
from codiet.model.flags import FlagFactory, FlagService
from codiet.model.nutrients import NutrientFactory
from codiet.model.tags import TagFactory
from codiet.model.time import TimeFactory
from codiet.model.ingredients import IngredientFactory
from codiet.model.recipes import RecipeFactory, Recipe
from codiet.optimisation import OptimiserFactory
from codiet.optimisation.constraints import ConstraintFactory

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(CURRENT_DIR, "json_data")

class BaseCodietTest(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.NUM_TAGS = 19

    def setUp(self) -> None:
        super().setUp()
        # REFACTOR: Wrap this up into some reusable method, that just
        # takes the TEST_DATA_DIR as an argument
        self.database_service = DatabaseService()
        self.json_repository = JSONRepository(TEST_DATA_DIR)        
        
        self.singleton_register = SingletonRegister()
        self.unit_conversion_service = UnitConversionService()
        self.flag_service = FlagService()

        self.quantities_factory = QuantitiesFactory()
        self.cost_factory = CostFactory()
        self.flag_factory = FlagFactory()
        self.nutrient_factory = NutrientFactory()
        self.tag_factory = TagFactory()
        self.time_factory = TimeFactory()
        self.ingredient_factory = IngredientFactory()
        self.recipe_factory = RecipeFactory()
        self.optimiser_factory = OptimiserFactory()
        self.constraint_factory = ConstraintFactory()

        self.optimiser_fixtures = OptimiserFixtures()
        self.recipe_fixtures = RecipeFixtures()

        Recipe.initialise(
            unit_conversion_service=self.unit_conversion_service,
            nutrient_factory=self.nutrient_factory,
            flag_factory=self.flag_factory,
            flag_service=self.flag_service
        )

        self.database_service.initialise(
            repository=self.json_repository,
            quantities_factory=self.quantities_factory,
            nutrients_factory=self.nutrient_factory,
            flag_factory=self.flag_factory,
            tag_factory=self.tag_factory,
            ingredient_factory=self.ingredient_factory,
            recipe_factory=self.recipe_factory
        )

        self.singleton_register.initialise(
            get_all_global_unit_conversion_names=self.database_service.read_all_global_unit_conversion_names,
            unit_loader=self.database_service.read_unit,
            global_unit_conversion_loader=self.database_service.read_global_unit_conversion,
            flag_definition_loader=self.database_service.read_flag_definition,
            nutrient_loader=self.database_service.read_nutrient,
            tag_graph_loader=self.database_service.read_all_tags,
            recipe_loader=self.database_service.read_recipe,
            ingredient_loader=self.database_service.read_ingredient
        )

        self.unit_conversion_service.initialise(
            create_quantity=self.quantities_factory.create_quantity,
            get_unit=self.singleton_register.get_unit,
            get_all_global_unit_conversions=lambda: self.singleton_register.global_unit_conversions
        )

        self.flag_service.initialise(
            create_flag=self.flag_factory.create_flag,
            get_flag_definition=self.singleton_register.get_flag_definition,
            get_all_flag_names=self.database_service.read_all_flag_names
        )

        # REFACTOR: Decouple further by only passing in specific methods
        self.quantities_factory.initialise(
            singleton_register=self.singleton_register,
            database_service=self.database_service
        )

        # REFACTOR: Decouple further by only passing in specific methods
        self.cost_factory.initialise(
            quantities_factory=self.quantities_factory
        )

        # REFACTOR: Decouple further by only passing in specific methods
        self.nutrient_factory.initialise(
            singleton_register=self.singleton_register,
            quantities_factory=self.quantities_factory
        )

        # REFACTOR: Decouple further by only passing in specific methods
        self.ingredient_factory.initialise(
            singleton_register=self.singleton_register,
            quantities_factory=self.quantities_factory,
            unit_conversion_service=self.unit_conversion_service,
            cost_factory=self.cost_factory,
            flag_factory=self.flag_factory,
            nutrient_factory=self.nutrient_factory
        )

        # REFACTOR: Decouple further by only passing in specific methods
        self.recipe_factory.initialise(
            singleton_register=self.singleton_register,
            unit_conversion_service=self.unit_conversion_service,
            quantities_factory=self.quantities_factory,
            time_factory=self.time_factory,
            flag_factory=self.flag_factory,
            ingredient_factory=self.ingredient_factory
        )

        # REFACTOR: Decouple further by only passing in specific methods
        self.optimiser_factory.initialise(
            database_service=self.database_service,
        )

        # REFACTOR: Decouple further by only passing in specific methods
        self.recipe_fixtures.initialise(
            recipe_factory=self.recipe_factory,
        )

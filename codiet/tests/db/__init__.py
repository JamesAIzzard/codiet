import os
import tempfile
import unittest

from codiet.db_population.units import get_global_units
from codiet.db_population.flags import get_global_flags
from codiet.db_population.nutrients import get_global_nutrients
from codiet.db_population.recipes.recipe_tags import get_global_recipe_tags
from codiet.db.database import Database
from codiet.db.repository import Repository
from codiet.db.database_service import DatabaseService
from codiet.models.ingredients import Ingredient
from codiet.models.recipes import Recipe

class DatabaseTestCase(unittest.TestCase):
    """Base class for Repository test cases."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_units_setup = False
        self.global_flags_setup = False
        self.global_nutrients_setup = False
        self.global_recipe_tags_setup = False

    def setUp(self):
        """Set up the test case."""
        # Create a temporary file for the database
        self.temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db_file.name
        # Init the database classes
        self.database = Database(db_path=self.db_path)
        self.repository = Repository(self.database)
        self.database_service = DatabaseService(self.repository)
        # Create the database
        self.database._create_database()

    def setup_global_units(self) -> None:
        """Populate the global units."""
        if not self.global_units_setup:
            global_units = get_global_units()
            self.database_service.create_global_units(global_units)
            self.global_flags_setup = True

    def setup_global_flags(self) -> None:
        """Populate the global flags."""
        if not self.global_flags_setup:
            global_flags = get_global_flags()
            self.database_service.create_global_flags(global_flags)
            self.global_flags_setup = True

    def setup_global_nutrients(self) -> None:
        """Populate the global nutrients."""
        if not self.global_units_setup:
            global_nutrients = get_global_nutrients()
            self.database_service.create_global_nutrients(global_nutrients)
            self.global_nutrients_setup = True

    def setup_global_recipe_tags(self) -> None:
        """Populate the global recipe tags."""
        if not self.global_recipe_tags_setup:
            global_recipe_tags = get_global_recipe_tags()
            self.database_service.create_global_recipe_tags(global_recipe_tags)
            self.global_recipe_tags_setup = True

    def setup_test_ingredient(self, ingredient_name:str) -> Ingredient:
        """Create a test ingredient."""
        # Setup the environment
        self.setup_global_units()
        self.setup_global_flags()
        self.setup_global_nutrients()
        self.unit_id_name_map = self.database_service.build_unit_name_id_map()
        self.flag_id_name_map = self.database_service.build_flag_name_id_map()
        self.nutrient_id_name_map = self.database_service.build_nutrient_name_id_map()
        # Create the test ingredient
        test_ingredient = self.database_service.create_empty_ingredient(ingredient_name=ingredient_name)
        # Update the description
        test_ingredient.description = "This is a test ingredient"
        self.database_service.repository.update_ingredient_description(
            ingredient_id=test_ingredient.id,
            description=test_ingredient.description
        )
        # Update the standard unit
        standard_unit_id = self.unit_id_name_map.get_int("gram")
        self.database_service.repository.update_ingredient_standard_unit_id(
            ingredient_id=test_ingredient.id,
            standard_unit_id=standard_unit_id
        )
        test_ingredient.standard_unit_id = standard_unit_id
        # Add a unit conversion
        slice_uc = self.database_service.create_ingredient_unit_conversion(
            ingredient_id=test_ingredient.id,
            from_unit_id=self.unit_id_name_map.get_int("slice"),
            to_unit_id=self.unit_id_name_map.get_int("gram"),
            from_unit_qty=1,
            to_unit_qty=150
        )
        test_ingredient.add_unit_conversion(slice_uc)
        # Update the cost
        self.database_service.repository.update_ingredient_cost(
            ingredient_id=test_ingredient.id,
            cost_value=1.0,
            cost_qty_value=100.0,
            cost_qty_unit_id=self.unit_id_name_map.get_int("gram"),
        )
        test_ingredient.cost_value = 1.0
        test_ingredient.cost_qty_value = 100.0
        test_ingredient.cost_qty_unit_id = self.unit_id_name_map.get_int("gram")
        # Set a couple of flags
        vegan_flag_id = self.flag_id_name_map.get_int("vegan")
        self.database_service.repository.create_ingredient_flag(
            ingredient_id=test_ingredient.id, 
            flag_id=vegan_flag_id,
            value=True
        )
        test_ingredient.set_flag(vegan_flag_id, True)
        vegetarian_flag_id = self.flag_id_name_map.get_int("vegetarian")
        self.database_service.repository.create_ingredient_flag(
            ingredient_id=test_ingredient.id, 
            flag_id=vegetarian_flag_id,
            value=True
        )
        test_ingredient.set_flag(vegetarian_flag_id, True)
        # Set the gylycemic index
        test_ingredient.gi = 50
        self.database_service.repository.update_ingredient_gi(
            ingredient_id=test_ingredient.id,
            gi=test_ingredient.gi
        )
        # Add a couple of nutrient quantities
        alanine_nq = self.database_service.create_ingredient_nutrient_quantity(
            ingredient_id=test_ingredient.id,
            nutrient_id=self.nutrient_id_name_map.get_int("alanine"),
            ntr_mass_unit_id=self.unit_id_name_map.get_int("milligram"),
            ntr_mass_value=100,
            ing_qty_unit_id=self.unit_id_name_map.get_int("slice"),
            ing_qty_value=1.0
        )
        test_ingredient.add_nutrient_quantity(alanine_nq)
        arginine_nq = self.database_service.create_ingredient_nutrient_quantity(
            ingredient_id=test_ingredient.id,
            nutrient_id=self.nutrient_id_name_map.get_int("arginine"),
            ntr_mass_unit_id=self.unit_id_name_map.get_int("milligram"),
            ntr_mass_value=200,
            ing_qty_unit_id=self.unit_id_name_map.get_int("ounce"),
            ing_qty_value=1.0
        )
        test_ingredient.add_nutrient_quantity(arginine_nq)
        return test_ingredient

    def setup_test_recipe(self, recipe_name:str) -> Recipe:
        """Create a test recipe."""
        # Setup the environment
        self.setup_global_units()
        self.setup_global_flags()
        self.setup_global_nutrients()
        self.setup_global_recipe_tags()
        self.unit_id_name_map = self.database_service.build_unit_name_id_map()
        self.flag_id_name_map = self.database_service.build_flag_name_id_map()
        self.nutrient_id_name_map = self.database_service.build_nutrient_name_id_map()
        self.recipe_tag_id_name_map = self.database_service.build_recipe_tag_name_id_map()
        # Create the test recipe
        test_recipe = self.database_service.create_empty_recipe(recipe_name=recipe_name)
        # Update use as ingredient
        test_recipe.use_as_ingredient = True
        self.database_service.repository.update_use_recipe_as_ingredient(
            recipe_id=test_recipe.id,
            use_as_ingredient=test_recipe.use_as_ingredient
        )
        # Update the description
        test_recipe.description = "This is a test recipe"
        self.database_service.repository.update_recipe_description(
            recipe_id=test_recipe.id,
            description=test_recipe.description
        )
        # Update the instructions
        test_recipe.instructions = "Here are some instructions for the test recipe."
        self.database_service.repository.update_recipe_instructions(
            recipe_id=test_recipe.id,
            instructions=test_recipe.instructions
        )
        # Add a couple of serve time windows
        stw1 = self.database_service.create_recipe_serve_time_window(
            recipe_id=test_recipe.id,
            window_string="06:00-09:00"
        )
        test_recipe.add_serve_time_window(stw1)
        stw2 = self.database_service.create_recipe_serve_time_window(
            recipe_id=test_recipe.id,
            window_string="12:00-14:00"
        )
        test_recipe.add_serve_time_window(stw2)
        # Add a couple of ingredient quantities
        # Create a couple of test ingredients
        test_ingredient_1 = self.setup_test_ingredient("Test Ingredient 1")
        test_ingredient_2 = self.setup_test_ingredient("Test Ingredient 2")
        # Add them to the recipe
        ingredient_qty_1 = self.database_service.create_recipe_ingredient_quantity(
            recipe_id=test_recipe.id,
            ingredient_id=test_ingredient_1.id,
            qty_unit_id=self.unit_id_name_map.get_int("slice"),
            qty_value=2.0,
            qty_ltol=0.1,
            qty_utol=0.1
        )
        test_recipe.add_ingredient_quantity(ingredient_quantity=ingredient_qty_1)
        ingredient_qty_2 = self.database_service.create_recipe_ingredient_quantity(
            recipe_id=test_recipe.id,
            ingredient_id=test_ingredient_2.id,
            qty_unit_id=self.unit_id_name_map.get_int("slice"),
            qty_value=1.0,
            qty_ltol=0.1,
            qty_utol=0.1
        )
        test_recipe.add_ingredient_quantity(ingredient_quantity=ingredient_qty_2)
        # Add a couple of recipe tags
        # Get the ids for a couple of tags
        tag_id_1 = self.recipe_tag_id_name_map.get_int("breakfast")
        tag_id_2 = self.recipe_tag_id_name_map.get_int("lunch")
        # Add the tags to the recipe
        self.database_service.repository.create_recipe_tag(
            recipe_id=test_recipe.id,
            global_tag_id=tag_id_1
        )
        test_recipe.add_recipe_tag(tag_id_1)
        self.database_service.repository.create_recipe_tag(
            recipe_id=test_recipe.id,
            global_tag_id=tag_id_2
        )
        test_recipe.add_recipe_tag(tag_id_2)
        return test_recipe

    def tearDown(self) -> None:
        """Tear down the test case."""
        self.repository.close_connection()
        self.temp_db_file.close()
        os.unlink(self.db_path)
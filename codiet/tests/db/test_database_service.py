from . import DatabaseTestCase
from codiet.db_population.units import get_global_units
from codiet.db_population.flags import get_global_flags
from codiet.db_population.nutrients import get_global_nutrients
from codiet.models.ingredients import Ingredient

def flatten_nutrients(nutrient_data, parent_id=None):
    """Flatten the nested nutrient structure into a list of nutrient dictionaries."""
    flattened = []

    def _flatten(nutrient_data, parent_id):
        for nutrient_name, nutrient_info in nutrient_data.items():
            nutrient = {
                "nutrient_name": nutrient_name,
                "aliases": nutrient_info.get("aliases", []),
                "parent_id": parent_id
            }
            flattened.append(nutrient)
            if "children" in nutrient_info:
                _flatten(nutrient_info["children"], nutrient_name)

    _flatten(nutrient_data, parent_id)
    return flattened

class TestCreateGlobalUnits(DatabaseTestCase):

    def test_create_global_units_creates_global_units(self):
        """Test creating global units in the database."""
        # Grab the JSON config data for the global units
        global_units = get_global_units()
        # Insert the global units
        self.database_service.create_global_units(global_units)
        # Fetch all the global units
        fetched_global_units = self.database_service.repository.read_all_global_units()
        # Fetch the map of unit names to unit IDs
        unit_name_to_id = self.database_service.build_unit_name_id_map()
        # Check the length of the fetched global units is the same as the global units
        self.assertEqual(len(fetched_global_units), len(global_units))
        # For each global unit,
        for global_unit_name in global_units.keys():
            # Grab the ID of the unit and check its in the fetched units
            unit_id = unit_name_to_id.get_int(global_unit_name)
            self.assertIn(unit_id, fetched_global_units)

class TestCreateGlobalFlags(DatabaseTestCase):

    def test_create_global_flags_create_global_flags(self):
        """Test creating global flags in the database."""
        # Get the global flags
        global_flags = get_global_flags()
        # Insert the global flags
        self.database_service.create_global_flags(global_flags)
        # Fetch all the global flags
        fetched_global_flags = self.database_service.repository.read_all_global_flags()
        # Check the length of the fetched global flags is the same as the global flags
        self.assertEqual(len(fetched_global_flags), len(global_flags))
        # For each global flag,
        for global_flag in global_flags:
            # Check the global flag is in the fetched global flags
            self.assertIn(global_flag, fetched_global_flags.values())

class TestCreateGlobalNutrients(DatabaseTestCase):

    def test_create_global_nutrients_creates_global_nutrients(self):
        """Test creating global nutrients."""
        # Get the global nutrients
        global_nutrients = get_global_nutrients()
        # Insert the global nutrients
        self.database_service.create_global_nutrients(global_nutrients)
        # Fetch all the global nutrients
        fetched_global_nutrients = self.database_service.repository.read_all_global_nutrients()
        # Flatten the original global nutrients structure
        flattened_nutrients = flatten_nutrients(global_nutrients)
        # Check each nutrient in the flattened list is in the fetched global nutrients
        for nutrient in flattened_nutrients:
            found = False
            for fetched_nutrient in fetched_global_nutrients.values():
                if (fetched_nutrient["nutrient_name"] == nutrient["nutrient_name"] and
                    fetched_nutrient["aliases"] == nutrient["aliases"]):
                    found = True
                    break
            self.assertTrue(found, f"Nutrient {nutrient} not found in fetched nutrients")

class TestCreateEmptyIngredient(DatabaseTestCase):

    def test_create_empty_ingredient_creates_empty_ingredient(self):
        """Test creating an empty ingredient."""
        # Configure the flags and nutrients
        self.database_service.create_global_flags(get_global_flags())
        self.database_service.create_global_nutrients(get_global_nutrients())
        # Check there are no ingredients in the database
        ingredients = self.database_service.repository.read_all_ingredient_names()
        self.assertEqual(len(ingredients), 0)
        # Create the empty ingredient
        ingredient_name = "Test Ingredient"        
        ingredient = self.database_service.create_empty_ingredient(ingredient_name)
        # Check the thing returned is an ingredient
        self.assertIsInstance(ingredient, Ingredient)
        # Check the name is set correctly
        self.assertEqual(ingredient.name, ingredient_name)
        # Check the id is set correctly
        self.assertEqual(ingredient.id, 1)
        # Check the description is None
        self.assertIsNone(ingredient.description)
        # Check the cost unit id is None
        self.assertIsNone(ingredient.cost_unit_id)
        # Check the cost value is None
        self.assertIsNone(ingredient.cost_value)
        # Check the cost quantity unit id is None
        self.assertIsNone(ingredient.cost_qty_unit_id)
        # Check the cost quantity value is None
        self.assertIsNone(ingredient.cost_qty_value)
        # Check the standard unit is None
        self.assertIsNone(ingredient.standard_unit_id)
        # Check there are no units
        self.assertEqual(len(ingredient.unit_conversions), 0)
        # Check there are no flags yet
        self.assertEqual(len(ingredient.flags), 0)
        # Check the gi is None
        self.assertIsNone(ingredient.gi)
        # Check there are no nutrients yet
        self.assertEqual(len(ingredient.nutrient_quantities), 0)

class TestCreateEmptyRecipe(DatabaseTestCase):

    def test_create_empty_recipe_creates_empty_recipe(self):
        """Test creating an empty recipe."""
        # Check there are no recipes in the database
        recipes = self.database_service.repository.read_all_recipe_names()
        self.assertEqual(len(recipes), 0)
        # Create the empty recipe
        recipe_name = "Test Recipe"
        recipe = self.database_service.create_empty_recipe(recipe_name)
        # Check the name is set correctly
        self.assertEqual(recipe.name, recipe_name)
        # Check the id is set correctly
        self.assertEqual(recipe.id, 1)
        # Check the description is None
        self.assertIsNone(recipe.description)
        # Check there are no instructions
        self.assertIsNone(recipe.instructions)
        # Check there are no ingredient quantities
        self.assertEqual(len(recipe.ingredient_quantities), 0)
        # Check there are no serve time windows
        self.assertEqual(len(recipe.serve_time_windows), 0)
        # Check there are no tags
        self.assertEqual(len(recipe.tags), 0)

class TestReadIngredient(DatabaseTestCase):

    def test_read_ingredient_reads_ingredient(self):
        """Test reading an ingredient."""
        # Configure the units, flags and nutrients
        self.database_service.create_global_units(get_global_units())
        self.database_service.create_global_flags(get_global_flags())
        self.database_service.create_global_nutrients(get_global_nutrients())
        # Fetch id name maps
        flag_name_to_id = self.database_service.build_flag_name_id_map()
        unit_name_to_id = self.database_service.build_unit_name_id_map()
        nutrient_name_to_id = self.database_service.build_nutrient_name_id_map()
        # Fetch the unit id for grams
        g_id = unit_name_to_id.get_int("gram")
        # Create an empty ingredient
        ingredient_name = "Test Ingredient"
        ingredient = self.database_service.create_empty_ingredient(ingredient_name)
        # Set the description
        description = "Test description"
        self.database_service.repository.update_ingredient_description(ingredient.id, description)
        # Set the cost data
        cost_value = 1.0
        cost_qty_unit_id = g_id
        cost_qty_value = 100.0
        self.database_service.repository.update_ingredient_cost(ingredient.id, cost_value, cost_qty_unit_id, cost_qty_value)
        # Set the standard unit id
        self.database_service.repository.update_ingredient_standard_unit_id(ingredient.id, g_id)
        # Set a couple of unit conversions
        # Grab the id for slice
        slice_id = unit_name_to_id.get_int("slice")
        # Create a unit conversion
        ing_slice_uc = self.database_service.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient.id,
            from_unit_id=g_id,
            to_unit_id=slice_id,
            from_unit_qty=150,
            to_unit_qty=1

        )
        # Set a couple of flags
        # Fetch the flag id for a couple of flags
        gf_flag_id = flag_name_to_id.get_int("gluten free")
        v_flag_id = flag_name_to_id.get_int("vegetarian")
        # Set them on the ingredient        
        self.database_service.repository.create_ingredient_flag(ingredient.id, gf_flag_id, True)
        self.database_service.repository.create_ingredient_flag(ingredient.id, v_flag_id, False)        
        # Set the GI
        gi = 50.0
        self.database_service.repository.update_ingredient_gi(ingredient.id, gi)
        # Grab the global id's for a nutrient
        alanine_id = nutrient_name_to_id.get_int("alanine")
        # Set these nutrient quantities on the ingredient
        self.database_service.repository.create_ingredient_nutrient_quantity(
            ingredient_id=ingredient.id,
            nutrient_id=alanine_id,
            ntr_mass_unit_id=g_id,
            ntr_mass_value=1.0,
            ing_qty_unit_id=slice_id,
            ing_qty_value=2.0
        )
        # Read the ingredient
        fetched_ingredient = self.database_service.read_ingredient(ingredient.id)
        # Check the thing returned is an ingredient
        self.assertIsInstance(fetched_ingredient, Ingredient)
        # Check the name is set correctly
        self.assertEqual(fetched_ingredient.name, ingredient_name)
        # Check the id is set correctly
        self.assertEqual(fetched_ingredient.id, ingredient.id)
        # Check the description is set correctly
        self.assertEqual(fetched_ingredient.description, description)
        # Check the cost value is set correctly
        self.assertEqual(fetched_ingredient.cost_value, cost_value)
        # Check the cost quantity unit id is set correctly
        self.assertEqual(fetched_ingredient.cost_qty_unit_id, cost_qty_unit_id)
        # Check the cost quantity value is set correctly
        self.assertEqual(fetched_ingredient.cost_qty_value, cost_qty_value)
        # Check the standard unit id is set correctly
        self.assertEqual(fetched_ingredient.standard_unit_id, g_id)
        # Check the unit conversions are set correctly
        self.assertEqual(len(fetched_ingredient.unit_conversions), 1)
        self.assertIn(ing_slice_uc, fetched_ingredient.unit_conversions.keys())
        # Check the flags are set correctly
        self.assertEqual(len(fetched_ingredient.flags), 2)
        self.assertIn(gf_flag_id, fetched_ingredient.flags.keys())
        self.assertIn(v_flag_id, fetched_ingredient.flags.keys())
        self.assertTrue(fetched_ingredient.flags[gf_flag_id])
        self.assertFalse(fetched_ingredient.flags[v_flag_id])
        # Check the gi is set correctly
        self.assertEqual(fetched_ingredient.gi, gi)
        # Check the nutrient quantities are set correctly
        self.assertEqual(len(fetched_ingredient.nutrient_quantities), 1)
        self.assertIn(alanine_id, fetched_ingredient.nutrient_quantities.keys())

class TestUpdateIngredient(DatabaseTestCase):

    def test_update_ingredient_updates_ingredient(self):
        """Test updating an ingredient."""
        # Configure the units, flags and nutrients
        self.database_service.create_global_units(get_global_units())
        self.database_service.create_global_flags(get_global_flags())
        self.database_service.create_global_nutrients(get_global_nutrients())
        # Fetch id name maps
        flag_name_to_id = self.database_service.build_flag_name_id_map()
        unit_name_to_id = self.database_service.build_unit_name_id_map()
        nutrient_name_to_id = self.database_service.build_nutrient_name_id_map()
        # Fetch the unit id for grams
        g_id = unit_name_to_id.get_int("gram")
        # Create an empty ingredient
        ingredient_name = "Test Ingredient"
        ingredient = self.database_service.create_empty_ingredient(ingredient_name)
        # Set the description
        description = "Test description"
        self.database_service.repository.update_ingredient_description(ingredient.id, description)
        # Set the cost data
        cost_value = 1.0
        cost_qty_unit_id = g_id
        cost_qty_value = 100.0
        self.database_service.repository.update_ingredient_cost(ingredient.id, cost_value, cost_qty_unit_id, cost_qty_value)
        # Set the standard unit id
        self.database_service.repository.update_ingredient_standard_unit_id(ingredient.id, g_id)
        # Set a couple of unit conversions
        # Grab the id for slice
        slice_id = unit_name_to_id.get_int("slice")
        # Create a unit conversion
        ing_slice_uc = self.database_service.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient.id,
            from_unit_id=g_id,
            to_unit_id=slice_id,
            from_unit_qty=150,
            to_unit_qty=1

        )
        # Set a couple of flags
        # Fetch the flag id for a couple of flags
        gf_flag_id = flag_name_to_id.get_int("gluten free")
        v_flag_id = flag_name_to_id.get_int("vegetarian")
        # Set them on the ingredient        
        ing_gf_flag_id = self.database_service.repository.create_ingredient_flag(ingredient.id, gf_flag_id, True)
        ing_v_flag_id = self.database_service.repository.create_ingredient_flag(ingredient.id, v_flag_id, False)        
        # Set the GI
        gi = 50.0
        self.database_service.repository.update_ingredient_gi(ingredient.id, gi)
        # Grab the global id's for a nutrient
        alanine_id = nutrient_name_to_id.get_int("alanine")
        # Set these nutrient quantities on the ingredient
        ing_alanine_id = self.database_service.repository.create_ingredient_nutrient_quantity(
            ingredient_id=ingredient.id,
            nutrient_id=alanine_id,
            ntr_mass_unit_id=g_id,
            ntr_mass_value=1.0,
            ing_qty_unit_id=slice_id,
            ing_qty_value=2.0
        )







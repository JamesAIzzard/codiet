from . import DatabaseTestCase
from codiet.db_population.units import read_global_units_from_json
from codiet.db_population.flags import get_global_flags
from codiet.db_population.nutrients import get_global_nutrients
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.entity_unit_conversion import EntityUnitConversion
from codiet.models.nutrients import Nutrient
from codiet.models.nutrients.entity_nutrient_quantity import EntityNutrientQuantity
from codiet.models.ingredients.ingredient import Ingredient
from codiet.models.ingredients.ingredient_quantity import IngredientQuantity
from codiet.models.time import RecipeServeTimeWindow

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
        """Test that create_global_units creates global units in the database."""
        # Grab the JSON config data for the global units
        json_global_units = read_global_units_from_json()
        # Insert the global units
        self.database_service.create_global_units(json_global_units)
        # Fetch all the global units
        fetched_global_units = self.database_service.repository.read_all_global_units()
        # Check the length of the fetched global units is the same as the global units
        self.assertEqual(len(fetched_global_units), len(json_global_units))
        # Fetch the map of unit names to unit IDs
        unit_id_to_name = self.database_service.unit_id_name_map
        # For each global unit,
        for global_unit_name in json_global_units.keys():
            # Grab the ID of the unit and check its in the fetched units
            unit_id = unit_id_to_name.get_keys(global_unit_name)[0]
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

class TestCreateIngredient(DatabaseTestCase):

    def test_create_ingredient_creates_empty_ingredient(self):
        """Test creating an empty ingredient."""
        # Configure the flags and nutrients
        self.database_service.create_global_flags(get_global_flags())
        self.database_service.create_global_nutrients(get_global_nutrients())
        self.database_service.create_global_units(read_global_units_from_json())    
        # Check there are no ingredients in the database
        ingredients = self.database_service.repository.read_all_ingredient_names()
        self.assertEqual(len(ingredients), 0)
        # Create the empty ingredient
        ingredient_name = "Test Ingredient"        
        ingredient = Ingredient(name=ingredient_name)
        ingredient = self.database_service.create_ingredient(ingredient)
        # Check the thing returned is an ingredient
        self.assertIsInstance(ingredient, Ingredient)
        # Check the name is set correctly
        self.assertEqual(ingredient.name, ingredient_name)
        # Check the id is set correctly
        self.assertEqual(ingredient.id, 1)
        # Check the description is None
        self.assertIsNone(ingredient.description)
        # Assert the standard unit is set to grams
        self.assertEqual(ingredient.standard_unit_id, self.database_service.gram_id)
        # Check the cost value is None
        self.assertIsNone(ingredient.cost_value)
        # Check the cost quantity unit id is grams
        self.assertEqual(ingredient.cost_qty_unit_id, self.database_service.gram_id)
        # Check the cost quantity value is None
        self.assertIsNone(ingredient.cost_qty_value)
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
        # Check use as ingredient is False
        self.assertFalse(recipe.use_as_ingredient)
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

class TestCreateRecipeIngredientQuantity(DatabaseTestCase):

    def test_create_recipe_ingredient_quantity_creates_recipe_ingredient_quantity(self):
        """Test creating a recipe ingredient quantity."""
        # Create an empty recipe
        recipe_name = "Test Recipe"
        recipe = self.database_service.create_empty_recipe(recipe_name)
        # Init the units
        self.database_service.create_global_units(read_global_units_from_json())
        # Create an empty ingredient
        ingredient_name = "Test Ingredient"
        ingredient = Ingredient(name=ingredient_name)
        ingredient = self.database_service.create_ingredient(ingredient)
        assert ingredient.id is not None
        # Create the recipe ingredient quantity
        riq = self.database_service.create_recipe_ingredient_quantity(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            qty_unit_id=self.database_service.gram_id,
            qty_value=100.0,
            qty_ltol=0.2,
            qty_utol=0.3
        )
        # Check the thing returned is a RecipeIngredientQuantity
        self.assertIsInstance(riq, IngredientQuantity)
        # Check the id is set correctly
        self.assertEqual(riq.id, 1)
        # Check the recipe id is set correctly
        self.assertEqual(riq.recipe_id, recipe.id)
        # Check the ingredient id is set correctly
        self.assertEqual(riq.ingredient_id, ingredient.id)
        # Check the quantity unit id is set correctly
        self.assertEqual(riq.qty_unit_id, self.database_service.gram_id)
        # Check the quantity value is set correctly
        self.assertEqual(riq.qty_value, 100.0)
        # Check the lower tolerance is set correctly
        self.assertEqual(riq.lower_tol, 0.2)
        # Check the upper tolerance is set correctly
        self.assertEqual(riq.upper_tol, 0.3)

class TestCreateRecipeServeTimeWindow(DatabaseTestCase):
    
        def test_create_recipe_serve_time_window_creates_recipe_serve_time_window(self):
            """Test creating a recipe serve time window."""
            # Create an empty recipe
            recipe_name = "Test Recipe"
            recipe = self.database_service.create_empty_recipe(recipe_name)
            # Confirm there are no serve time windows associated with the recipe
            time_windows = self.database_service.repository.read_recipe_serve_time_windows(recipe.id)
            self.assertEqual(len(time_windows), 0)
            # Create the recipe serve time window
            window_string = "08:00-09:00"
            serve_time_window = self.database_service.create_recipe_serve_time_window(recipe.id, window_string)
            # Check the thing returned is a RecipeServeTimeWindow
            self.assertIsInstance(serve_time_window, RecipeServeTimeWindow)
            # Check the id is set correctly
            self.assertEqual(serve_time_window.id, 1)
            # Check the recipe id is set correctly
            self.assertEqual(serve_time_window.recipe_id, recipe.id)
            # Check the window string is set correctly
            self.assertEqual(serve_time_window.window_string, window_string)


class TestReadGlobalUnit(DatabaseTestCase):

    def test_read_global_unit_reads_global_unit(self):
        """Test reading a global unit."""
        # Create a global unit
        unit_name = "Test Unit"
        unit_id = self.database_service.repository.create_global_unit(
            unit_name=unit_name,
            single_display_name="Test Unit",
            plural_display_name="Test Units",
            unit_type="mass",
            aliases=["test alias"]
        )
        # Read the global unit
        fetched_unit = self.database_service.read_global_unit(unit_id)
        # Check the thing returned is a unit
        self.assertIsInstance(fetched_unit, Unit)
        # Check the name is set correctly
        self.assertEqual(fetched_unit.unit_name, unit_name)
        # Check the id is set correctly
        self.assertEqual(fetched_unit.id, unit_id)
        # Check the single display name is set correctly
        self.assertEqual(fetched_unit.single_display_name, "Test Unit")
        # Check the plural display name is set correctly
        self.assertEqual(fetched_unit.plural_display_name, "Test Units")
        # Check the unit type is set correctly
        self.assertEqual(fetched_unit.type, "mass")
        # Check the aliases are set correctly
        self.assertEqual(fetched_unit.aliases, ["test alias"])

class TestReadAllGlobalUnits(DatabaseTestCase):

    def test_read_all_global_units_reads_all_global_units(self):
        """Test reading all global units."""
        # Create a couple of global units
        unit_name_1 = "Test Unit 1"
        unit_id_1 = self.database_service.repository.create_global_unit(
            unit_name=unit_name_1,
            single_display_name="Test Unit 1",
            plural_display_name="Test Units 1",
            unit_type="mass",
            aliases=["test alias 1.1, test alias 1.2"]
        )
        unit_name_2 = "Test Unit 2"
        unit_id_2 = self.database_service.repository.create_global_unit(
            unit_name=unit_name_2,
            single_display_name="Test Unit 2",
            plural_display_name="Test Units 2",
            unit_type="volume",
            aliases=["test alias 2.1, test alias 2.2"]
        )
        # Read all the global units
        fetched_global_units = self.database_service.read_all_global_units()
        # Check the length of the fetched global units is the same as the number of created global units
        self.assertEqual(len(fetched_global_units), 2)
        # Check the global units are in the fetched global units
        self.assertIn(unit_id_1, fetched_global_units)
        self.assertIn(unit_id_2, fetched_global_units)
        # Check that both are units
        self.assertIsInstance(fetched_global_units[unit_id_1], Unit)
        self.assertIsInstance(fetched_global_units[unit_id_2], Unit)
        # Check the data is correct for unit 1
        self.assertEqual(fetched_global_units[unit_id_1].unit_name, unit_name_1)
        self.assertEqual(fetched_global_units[unit_id_1].single_display_name, "Test Unit 1")
        self.assertEqual(fetched_global_units[unit_id_1].plural_display_name, "Test Units 1")
        self.assertEqual(fetched_global_units[unit_id_1].type, "mass")
        self.assertEqual(fetched_global_units[unit_id_1].aliases, ["test alias 1.1, test alias 1.2"])
        # Check the data is correct for unit 2
        self.assertEqual(fetched_global_units[unit_id_2].unit_name, unit_name_2)
        self.assertEqual(fetched_global_units[unit_id_2].single_display_name, "Test Unit 2")
        self.assertEqual(fetched_global_units[unit_id_2].plural_display_name, "Test Units 2")
        self.assertEqual(fetched_global_units[unit_id_2].type, "volume")
        self.assertEqual(fetched_global_units[unit_id_2].aliases, ["test alias 2.1, test alias 2.2"])

class TestReadAllGlobalMassUnits(DatabaseTestCase):
    
        def test_read_all_global_mass_units_reads_all_global_mass_units(self):
            """Test reading all global mass units."""
            # Create three units, two of which are mass units
            unit_name_1 = "Test Unit 1"
            unit_id_1 = self.database_service.repository.create_global_unit(
                unit_name=unit_name_1,
                single_display_name="Test Unit 1",
                plural_display_name="Test Units 1",
                unit_type="mass",
                aliases=["test alias 1.1, test alias 1.2"]
            )
            unit_name_2 = "Test Unit 2"
            unit_id_2 = self.database_service.repository.create_global_unit(
                unit_name=unit_name_2,
                single_display_name="Test Unit 2",
                plural_display_name="Test Units 2",
                unit_type="volume",
                aliases=["test alias 2.1, test alias 2.2"]
            )
            unit_name_3 = "Test Unit 3"
            unit_id_3 = self.database_service.repository.create_global_unit(
                unit_name=unit_name_3,
                single_display_name="Test Unit 3",
                plural_display_name="Test Units 3",
                unit_type="mass",
                aliases=["test alias 3.1, test alias 3.2"]
            )

            # Read all the global mass units
            fetched_global_mass_units = self.database_service.read_all_global_mass_units()
            # Check the length of the fetched global mass units is the same as the number of created global mass units
            self.assertEqual(len(fetched_global_mass_units), 2)
            # Check the global mass units are in the fetched global mass units
            self.assertIn(unit_id_1, fetched_global_mass_units)
            self.assertIn(unit_id_3, fetched_global_mass_units)
            self.assertNotIn(unit_id_2, fetched_global_mass_units)
            # Check that the unit is a mass unit
            self.assertIsInstance(fetched_global_mass_units[unit_id_1], Unit)
            self.assertIsInstance(fetched_global_mass_units[unit_id_3], Unit)
            # Check the data is correct for unit 1
            self.assertEqual(fetched_global_mass_units[unit_id_1].unit_name, unit_name_1)
            self.assertEqual(fetched_global_mass_units[unit_id_1].single_display_name, "Test Unit 1")
            self.assertEqual(fetched_global_mass_units[unit_id_1].plural_display_name, "Test Units 1")
            self.assertEqual(fetched_global_mass_units[unit_id_1].type, "mass")
            self.assertEqual(fetched_global_mass_units[unit_id_1].aliases, ["test alias 1.1, test alias 1.2"])
            # Check the data is correct for unit 3
            self.assertEqual(fetched_global_mass_units[unit_id_3].unit_name, unit_name_3)
            self.assertEqual(fetched_global_mass_units[unit_id_3].single_display_name, "Test Unit 3")
            self.assertEqual(fetched_global_mass_units[unit_id_3].plural_display_name, "Test Units 3")
            self.assertEqual(fetched_global_mass_units[unit_id_3].type, "mass")
            self.assertEqual(fetched_global_mass_units[unit_id_3].aliases, ["test alias 3.1, test alias 3.2"])

class TestReadAllGlobalUnitConversions(DatabaseTestCase):
    
        def test_read_all_global_unit_conversions_reads_all_global_unit_conversions(self):
            """Test reading all global unit conversions."""
            # Create a couple of global units
            unit_name_1 = "Test Unit 1"
            unit_id_1 = self.database_service.repository.create_global_unit(
                unit_name=unit_name_1,
                single_display_name="Test Unit 1",
                plural_display_name="Test Units 1",
                unit_type="mass",
                aliases=["test alias 1.1, test alias 1.2"]
            )
            unit_name_2 = "Test Unit 2"
            unit_id_2 = self.database_service.repository.create_global_unit(
                unit_name=unit_name_2,
                single_display_name="Test Unit 2",
                plural_display_name="Test Units 2",
                unit_type="volume",
                aliases=["test alias 2.1, test alias 2.2"]
            )
            # Create a couple of unit conversions
            uc1id = self.database_service.repository.create_global_unit_conversion(
                from_unit_id=unit_id_1,
                to_unit_id=unit_id_2,
                from_unit_qty=1,
                to_unit_qty=2
            )
            uc2id = self.database_service.repository.create_global_unit_conversion(
                from_unit_id=unit_id_2,
                to_unit_id=unit_id_1,
                from_unit_qty=2,
                to_unit_qty=1
            )
            # Read all the global unit conversions
            fetched_global_unit_conversions = self.database_service.read_all_global_unit_conversions()
            # Check the length of the fetched global unit conversions is the same as the number of created global unit conversions
            self.assertEqual(len(fetched_global_unit_conversions), 2)
            # Check the global unit conversions are in the fetched global unit conversions
            self.assertIn(uc1id, fetched_global_unit_conversions)
            self.assertIn(uc2id, fetched_global_unit_conversions)
            # Check that both are unit conversions
            self.assertIsInstance(fetched_global_unit_conversions[uc1id], UnitConversion)
            self.assertIsInstance(fetched_global_unit_conversions[uc2id], UnitConversion)
            # Check the data is correct for unit conversion 1
            self.assertEqual(fetched_global_unit_conversions[uc1id].from_unit_id, unit_id_1)
            self.assertEqual(fetched_global_unit_conversions[uc1id].to_unit_id, unit_id_2)
            self.assertEqual(fetched_global_unit_conversions[uc1id].from_unit_qty, 1)
            self.assertEqual(fetched_global_unit_conversions[uc1id].to_unit_qty, 2)
            # Check the data is correct for unit conversion 2
            self.assertEqual(fetched_global_unit_conversions[uc2id].from_unit_id, unit_id_2)
            self.assertEqual(fetched_global_unit_conversions[uc2id].to_unit_id, unit_id_1)
            self.assertEqual(fetched_global_unit_conversions[uc2id].from_unit_qty, 2)
            self.assertEqual(fetched_global_unit_conversions[uc2id].to_unit_qty, 1)

class TestReadAllNutrients(DatabaseTestCase):

    def test_read_all_nutrients_reads_all_nutrients(self):
        """Test reading all nutrients."""
        # Create a small tree of nutrients
        nutrient_name_1 = "Test Nutrient 1"
        nutrient_id_1 = self.database_service.repository.create_global_nutrient(nutrient_name_1)
        nutrient_name_2 = "Test Nutrient 2"
        nutrient_id_2 = self.database_service.repository.create_global_nutrient(nutrient_name_2)
        nutrient_name_3 = "Test Nutrient 3"
        nutrient_id_3 = self.database_service.repository.create_global_nutrient(
            name=nutrient_name_3,
            parent_id=nutrient_id_1
        )
        # Read all the nutrients
        fetched_nutrients = self.database_service.read_all_global_nutrients()
        # Check the length of the fetched nutrients is the same as the number of created nutrients
        self.assertEqual(len(fetched_nutrients), 3)
        # Check the nutrients are in the fetched nutrients
        self.assertIn(nutrient_id_1, fetched_nutrients)
        self.assertIn(nutrient_id_2, fetched_nutrients)
        self.assertIn(nutrient_id_3, fetched_nutrients)
        # Check that all are nutrients
        self.assertIsInstance(fetched_nutrients[nutrient_id_1], Nutrient)
        self.assertIsInstance(fetched_nutrients[nutrient_id_2], Nutrient)
        self.assertIsInstance(fetched_nutrients[nutrient_id_3], Nutrient)
        # Check the data is correct for nutrient 1
        self.assertEqual(fetched_nutrients[nutrient_id_1].nutrient_name, nutrient_name_1)
        self.assertEqual(fetched_nutrients[nutrient_id_1].parent_id, None)
        self.assertEqual(fetched_nutrients[nutrient_id_1].child_ids, [nutrient_id_3])
        # Check the data is correct for nutrient 2
        self.assertEqual(fetched_nutrients[nutrient_id_2].nutrient_name, nutrient_name_2)
        self.assertEqual(fetched_nutrients[nutrient_id_2].parent_id, None)
        self.assertEqual(fetched_nutrients[nutrient_id_2].child_ids, [])
        # Check the data is correct for nutrient 3
        self.assertEqual(fetched_nutrients[nutrient_id_3].nutrient_name, nutrient_name_3)
        self.assertEqual(fetched_nutrients[nutrient_id_3].parent_id, nutrient_id_1)
        self.assertEqual(fetched_nutrients[nutrient_id_3].child_ids, [])

class TestReadIngredient(DatabaseTestCase):

    def test_read_ingredient_reads_ingredient(self):
        """Test reading an ingredient."""
        # Configure the units, flags and nutrients
        self.database_service.create_global_units(read_global_units_from_json())
        self.database_service.create_global_flags(get_global_flags())
        self.database_service.create_global_nutrients(get_global_nutrients())
        # Create an empty ingredient
        ingredient_name = "Test Ingredient"
        ingredient = Ingredient(name=ingredient_name)
        ingredient = self.database_service.create_ingredient(ingredient)
        assert ingredient.id is not None
        # Set the description
        description = "Test description"
        self.database_service.repository.update_ingredient_description(ingredient.id, description)
        # Set the cost data
        cost_value = 1.0
        cost_qty_unit_id = self.database_service.gram_id
        cost_qty_value = 100.0
        self.database_service.repository.update_ingredient_cost(ingredient.id, cost_value, cost_qty_unit_id, cost_qty_value)
        # Set the standard unit id
        self.database_service.repository.update_ingredient_standard_unit_id(ingredient.id, self.database_service.gram_id)
        # Set a couple of unit conversions
        # Grab the id for slice
        slice_id = self.database_service.unit_id_name_map.get_key("slice")
        # Create a unit conversion
        ing_slice_uc = self.database_service.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient.id,
            from_unit_id=self.database_service.gram_id,
            to_unit_id=slice_id,
            from_unit_qty=150,
            to_unit_qty=1

        )
        # Set a couple of flags
        # Fetch the flag id for a couple of flags
        gf_flag_id = flag_name_to_id.get_key("gluten free")
        v_flag_id = flag_name_to_id.get_key("vegetarian")
        # Assert neither are None
        assert gf_flag_id is not None
        assert v_flag_id is not None
        # Set them on the ingredient        
        self.database_service.repository.create_ingredient_flag(ingredient.id, gf_flag_id, True)
        self.database_service.repository.create_ingredient_flag(ingredient.id, v_flag_id, False)        
        # Set the GI
        gi = 50.0
        self.database_service.repository.update_ingredient_gi(ingredient.id, gi)
        # Grab the global id's for a nutrient
        alanine_id = nutrient_name_to_id.get_key("alanine")
        assert alanine_id is not None
        # Set these nutrient quantities on the ingredient
        self.database_service.repository.create_ingredient_nutrient_quantity(
            ingredient_id=ingredient.id,
            global_nutrient_id=alanine_id,
            ntr_mass_unit_id=g_id,
            ntr_mass_qty=1.0,
            ing_grams_qty=100.0
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

class TestUpdateIngredientUnitConversion(DatabaseTestCase):

    def test_update_ingredient_unit_conversion_updates_ingredient_unit_conversion(self):
        """Test updating an ingredient unit conversion."""
        # Create four units
        unit_name_1 = "gram"
        unit_id_1 = self.repository.create_global_unit(
            unit_name=unit_name_1,
            single_display_name="g",
            plural_display_name="g",
            unit_type="mass"
        )
        unit_name_2 = "Test Unit 2"
        unit_id_2 = self.repository.create_global_unit(
            unit_name=unit_name_2,
            single_display_name="Test Unit 2",
            plural_display_name="Test Units 2",
            unit_type="mass"
        )
        unit_name_3 = "Test Unit 3"
        unit_id_3 = self.repository.create_global_unit(
            unit_name=unit_name_3,
            single_display_name="Test Unit 3",
            plural_display_name="Test Units 3",
            unit_type="mass"
        )
        unit_name_4 = "Test Unit 4"
        unit_id_4 = self.repository.create_global_unit(
            unit_name=unit_name_4,
            single_display_name="Test Unit 4",
            plural_display_name="Test Units 4",
            unit_type="mass"
        )
        # Create an empty ingredient
        ingredient_name = "Test Ingredient"
        ingredient = Ingredient(ingredient_name)
        ingredient = self.database_service.create_ingredient(ingredient)
        assert ingredient.id is not None
        # Set a couple of unit conversions
        # Create conversions between 1 and 2 and 1 and 3
        uc1id = self.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient.id,
            from_unit_id=unit_id_1,
            to_unit_id=unit_id_2,
            from_unit_qty=1,
            to_unit_qty=2
        )
        uc2id = self.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient.id,
            from_unit_id=unit_id_1,
            to_unit_id=unit_id_3,
            from_unit_qty=1,
            to_unit_qty=3
        )
        # Check both of these conversions are in the database correctly
        ing_ucs = self.database_service.read_ingredient_unit_conversions(ingredient.id)
        self.assertEqual(len(ing_ucs), 2)
        self.assertIn(uc1id, ing_ucs)
        self.assertIn(uc2id, ing_ucs)
        # Check the values on both of these
        self.assertEqual(ing_ucs[uc1id].from_unit_id, unit_id_1)
        self.assertEqual(ing_ucs[uc1id].to_unit_id, unit_id_2)
        self.assertEqual(ing_ucs[uc1id].from_unit_qty, 1)
        self.assertEqual(ing_ucs[uc1id].to_unit_qty, 2)
        self.assertEqual(ing_ucs[uc2id].from_unit_id, unit_id_1)
        self.assertEqual(ing_ucs[uc2id].to_unit_id, unit_id_3)
        self.assertEqual(ing_ucs[uc2id].from_unit_qty, 1)
        self.assertEqual(ing_ucs[uc2id].to_unit_qty, 3)
        # Update the first unit conversion
        ing_ucs[uc1id].from_unit_id = unit_id_4
        ing_ucs[uc1id].to_unit_id = unit_id_3
        ing_ucs[uc1id].from_unit_qty = 2
        ing_ucs[uc1id].to_unit_qty = 1
        self.database_service.update_ingredient_unit_conversion(ing_ucs[uc1id])
        # Check the values on the first unit conversion are updated
        ing_ucs = self.database_service.read_ingredient_unit_conversions(ingredient.id)
        self.assertEqual(ing_ucs[uc1id].from_unit_id, unit_id_4)
        self.assertEqual(ing_ucs[uc1id].to_unit_id, unit_id_3)
        self.assertEqual(ing_ucs[uc1id].from_unit_qty, 2)
        self.assertEqual(ing_ucs[uc1id].to_unit_qty, 1)

class TestUpdateIngredient(DatabaseTestCase):

    def test_update_ingredient_updates_ingredient(self):
        """Test updating an ingredient."""
        # Configure the units, flags, and nutrients
        self.database_service.create_global_units(read_global_units_from_json())
        self.database_service.create_global_flags(get_global_flags())
        self.database_service.create_global_nutrients(get_global_nutrients())
        
        # Fetch id name maps
        flag_name_to_id = self.database_service.build_flag_name_id_map()
        unit_name_to_id = self.database_service.build_unit_name_id_map()
        nutrient_name_to_id = self.database_service.build_nutrient_name_id_map()
        
        # Fetch the unit id for grams
        g_id = unit_name_to_id.get_key("gram")
        assert g_id is not None
        
        # Create an empty ingredient
        ingredient_name = "Test Ingredient"
        ingredient = Ingredient(name=ingredient_name)
        ingredient = self.database_service.create_ingredient(ingredient)
        
        # Initial checks for default values
        self.assertEqual(ingredient.name, ingredient_name)
        self.assertIsNone(ingredient.description)
        self.assertIsNone(ingredient.cost_value)
        self.assertEqual(ingredient.cost_qty_unit_id, g_id)
        self.assertIsNone(ingredient.cost_qty_value)
        self.assertEqual(ingredient.standard_unit_id, g_id)
        self.assertEqual(len(ingredient.unit_conversions), 0)
        self.assertEqual(len(ingredient.flags), 0)
        self.assertIsNone(ingredient.gi)
        self.assertEqual(len(ingredient.nutrient_quantities), 0)
        
        # Set initial properties
        ingredient.description = "Test description"
        ingredient.cost_value = 1.0
        ingredient.cost_qty_unit_id = g_id
        ingredient.cost_qty_value = 100.0
        ingredient.standard_unit_id = g_id
        ingredient.gi = 50.0
        
        # Add unit conversion
        slice_id = unit_name_to_id.get_key("slice")
        assert slice_id is not None
        slice_uc_id = self.database_service.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient.id,
            from_unit_id=g_id,
            to_unit_id=slice_id,
            from_unit_qty=150,
            to_unit_qty=1
        )
        ing_slice_uc = EntityUnitConversion(
            id=slice_uc_id,
            entity_id=ingredient.id,
            from_unit_id=g_id,
            to_unit_id=slice_id,
            from_unit_qty=150,
            to_unit_qty=1
        )
        ingredient.add_unit_conversion(ing_slice_uc)
        
        # Add flags
        gf_flag_id = flag_name_to_id.get_key("gluten free")
        v_flag_id = flag_name_to_id.get_key("vegetarian")
        assert gf_flag_id is not None
        assert v_flag_id is not None
        ingredient.add_flag(gf_flag_id, True)
        ingredient.add_flag(v_flag_id, False)
        
        # Set nutrient quantities
        alanine_id = nutrient_name_to_id.get_key("alanine")
        assert alanine_id is not None
        ing_alanine_qty = EntityNutrientQuantity(
            id=alanine_id,
            entity_id=ingredient.id,
            nutrient_id=alanine_id,
            ntr_mass_unit_id=g_id,
            entity_grams_qty=100.0
        )
        ingredient.add_nutrient_quantity(ing_alanine_qty)
        
        # Update the ingredient in the database
        self.database_service.update_ingredient(ingredient)
        
        # Fetch the updated ingredient
        fetched_ingredient = self.database_service.read_ingredient(ingredient.id)
        
        # Verify initial properties
        self.assertEqual(fetched_ingredient.name, ingredient_name)
        self.assertEqual(fetched_ingredient.description, "Test description")
        self.assertEqual(fetched_ingredient.cost_value, 1.0)
        self.assertEqual(fetched_ingredient.cost_qty_unit_id, g_id)
        self.assertEqual(fetched_ingredient.cost_qty_value, 100.0)
        self.assertEqual(fetched_ingredient.standard_unit_id, g_id)
        self.assertEqual(fetched_ingredient.gi, 50.0)
        
        # Verify unit conversions
        self.assertEqual(len(fetched_ingredient.unit_conversions), 1)
        self.assertIn(ing_slice_uc, fetched_ingredient.unit_conversions.values())
        
        # Verify flags
        self.assertEqual(len(fetched_ingredient.flags), 2)
        self.assertTrue(fetched_ingredient.flags[gf_flag_id])
        self.assertFalse(fetched_ingredient.flags[v_flag_id])
        
        # Verify nutrient quantities
        self.assertEqual(len(fetched_ingredient.nutrient_quantities), 1)
        self.assertIn(alanine_id, fetched_ingredient.nutrient_quantities.keys())
        
        # Update the ingredient properties
        fetched_ingredient.name = "New Ingredient Name"
        fetched_ingredient.description = "New description"
        fetched_ingredient.cost_value = 2.0
        fetched_ingredient.gi = 60.0
        
        # Use the update method
        self.database_service.update_ingredient(fetched_ingredient)
        
        # Fetch the updated ingredient again
        updated_ingredient = self.database_service.read_ingredient(fetched_ingredient.id)
        
        # Verify the updates
        self.assertEqual(updated_ingredient.name, "New Ingredient Name")
        self.assertEqual(updated_ingredient.description, "New description")
        self.assertEqual(updated_ingredient.cost_value, 2.0)
        self.assertEqual(updated_ingredient.gi, 60.0)

class TestDeleteIngredientUnitConversions(DatabaseTestCase):

    def test_delete_ingredient_unit_conversions_deletes_ingredient_unit_conversions(self):
        """Test deleting ingredient unit conversions."""
        # Create three units
        unit_name_1 = "gram"
        unit_id_1 = self.repository.create_global_unit(
            unit_name=unit_name_1,
            single_display_name="g",
            plural_display_name="g",
            unit_type="mass"
        )
        unit_name_2 = "Test Unit 2"
        unit_id_2 = self.repository.create_global_unit(
            unit_name=unit_name_2,
            single_display_name="Test Unit 2",
            plural_display_name="Test Units 2",
            unit_type="mass"
        )
        unit_name_3 = "Test Unit 3"
        unit_id_3 = self.repository.create_global_unit(
            unit_name=unit_name_3,
            single_display_name="Test Unit 3",
            plural_display_name="Test Units 3",
            unit_type="mass"
        )
        # Create an empty ingredient
        ingredient_name = "Test Ingredient"
        ingredient = Ingredient(name=ingredient_name)
        ingredient = self.database_service.create_ingredient(ingredient)
        # Set a couple of unit conversions
        # Create conversions between 1 and 2 and 1 and 3
        uc1id = self.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient.id,
            from_unit_id=unit_id_1,
            to_unit_id=unit_id_2,
            from_unit_qty=1,
            to_unit_qty=2
        )
        uc2id = self.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient.id,
            from_unit_id=unit_id_1,
            to_unit_id=unit_id_3,
            from_unit_qty=1,
            to_unit_qty=3
        )
        # Check both of these conversions are in the database
        ing_ucs = self.database_service.repository.read_ingredient_unit_conversions(ingredient.id)
        self.assertEqual(len(ing_ucs), 2)
        self.assertIn(uc1id, ing_ucs)
        self.assertIn(uc2id, ing_ucs)
        # Delete the ingredient unit conversions
        self.database_service.delete_ingredient_unit_conversions(ingredient.id)
        # Check there are no unit conversions left
        ing_ucs = self.database_service.repository.read_ingredient_unit_conversions(ingredient.id)
        self.assertEqual(len(ing_ucs), 0)






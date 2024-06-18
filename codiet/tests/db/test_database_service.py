import unittest

from . import DatabaseTestCase
from codiet.utils.nutrients import find_leaf_nutrient_names
from codiet.db_population.flags import get_global_flags
from codiet.db_population.nutrients import get_global_nutrients
from codiet.models.ingredients import Ingredient
from codiet.models.nutrients import IngredientNutrientQuantity

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

class TestInsertGlobalFlags(DatabaseTestCase):

    def test_insert_global_flags_inserts_global_flags(self):
        """Test inserting global flags."""
        # Get the global flags
        global_flags = get_global_flags()
        # Insert the global flags
        self.database_service.insert_global_flags(global_flags)
        # Fetch all the global flags
        fetched_global_flags = self.database_service.repository.fetch_all_global_flags()
        # Check the length of the fetched global flags is the same as the global flags
        self.assertEqual(len(fetched_global_flags), len(global_flags))
        # For each global flag,
        for global_flag in global_flags:
            # Check the global flag is in the fetched global flags
            self.assertIn(global_flag, fetched_global_flags.values())

class TestInsertGlobalNutrients(DatabaseTestCase):

    def test_insert_global_nutrients_inserts_global_nutrients(self):
        """Test inserting global nutrients."""
        # Get the global nutrients
        global_nutrients = get_global_nutrients()
        # Insert the global nutrients
        self.database_service.insert_global_nutrients(global_nutrients)
        # Fetch all the global nutrients
        fetched_global_nutrients = self.database_service.repository.fetch_all_global_nutrients()
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
        self.database_service.insert_global_flags(get_global_flags())
        self.database_service.insert_global_nutrients(get_global_nutrients())
        # Check there are no ingredients in the database
        ingredients = self.database_service.repository.fetch_all_ingredient_names()
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
        # Check there are no units
        self.assertEqual(len(ingredient.units), 0)
        # Read all of the global flags
        flags = self.database_service.repository.fetch_all_global_flags()
        # Check each flag is present on the ingredient, and is set to None
        for flag_id in flags.keys():
            self.assertIsNone(ingredient.flags[flag_id])
        # Check the gi is None
        self.assertIsNone(ingredient.gi)
        # Check the nutrient quantities
        # First, get a list of all leaf nutrient names
        leaf_nutrient_names = find_leaf_nutrient_names(get_global_nutrients())
        # Check the leaf nutrient name list is the same length as the ingredient nutrient list
        self.assertEqual(len(leaf_nutrient_names), len(ingredient.nutrient_quantities))
        # Fetch the name-id map for the global nutrients
        nutrient_name_id_map = self.database_service.fetch_nutrient_id_name_map()
        # Work through each nutrient quantity on the ingredient
        for nutrient_qty in ingredient.nutrient_quantities.values():
            # Check the nutrient quantity is an instance of IngredientNutrientQuantity
            self.assertIsInstance(nutrient_qty, IngredientNutrientQuantity)
            # Check that the id is in the nutrient name id map
            self.assertIn(nutrient_qty.global_nutrient_id, nutrient_name_id_map.int_values)
            # Check the nutrient mass value is None
            self.assertIsNone(nutrient_qty.nutrient_mass_value)
            # Check the nutrient mass unit id is None
            self.assertIsNone(nutrient_qty.nutrient_mass_unit_id)
            # Check the ingredient quantity value is None
            self.assertIsNone(nutrient_qty.ingredient_quantity_value)
            # Check the ingredient quantity unit id is None
            self.assertIsNone(nutrient_qty.ingredient_quantity_unit_id)

        






import unittest

from . import get_repository

class RepositoryTestCase(unittest.TestCase):
    """Base class for Repository test cases."""

    def setUp(self):
        """Set up the test case."""
        self.repository = get_repository()
        self.repository.database.reset_database()

    def tearDown(self) -> None:
        """Tear down the test case."""
        self.repository.close_connection()

class TestInsertGlobalUnit(RepositoryTestCase):
    """Test the insert_global_unit method of the Repository class."""

    def test_insert_global_unit_inserts_unit(self):
        """Test that the method inserts a global unit into the database."""
        # Create a gram measurement unit
        g_id = self.repository.insert_global_unit(
            unit_name='gram',
            plural_name='grams',
            unit_type='mass',
            aliases=['g'],
        )
        # Create a kg measurement unit
        kg_id = self.repository.insert_global_unit(
            unit_name='kilogram',
            plural_name='kilograms',
            unit_type='mass',
            aliases=['kg'],
            conversions={g_id: 1000}
        )
        # Check that both gram and kg units are in the database
        # Grab a list of global units
        global_units = self.repository.fetch_all_global_units()
        # Assert that the unit names are there
        self.assertEqual(global_units[g_id]["unit_name"], 'gram')
        self.assertEqual(global_units[kg_id]["unit_name"], 'kilogram')
        # Assert that the plural names are there
        self.assertEqual(global_units[g_id]["plural_name"], 'grams')
        self.assertEqual(global_units[kg_id]["plural_name"], 'kilograms')
        # Assert the unit types are correct
        self.assertEqual(global_units[g_id]["unit_type"], 'mass')
        self.assertEqual(global_units[kg_id]["unit_type"], 'mass')
        # Assert the aliases are there
        self.assertIn('g', global_units[g_id]["aliases"])
        self.assertIn('kg', global_units[kg_id]["aliases"])
        # Assert the conversions are there
        self.assertEqual(global_units[kg_id]["conversions"][g_id], 1000)
        self.assertEqual(global_units[g_id]["conversions"], {})


class TestInsertGlobalFlag(RepositoryTestCase):
    """Test the insert_global_flag method of the Repository class."""

    def test_insert_global_flag_inserts_flag(self):
        """Test that the method inserts a global flag into the database."""
        flag_name = 'test_flag'

        self.repository.insert_global_flag(flag_name)

        self.assertIn(flag_name, self.repository.fetch_all_global_flags())

class TestInsertGlobalNutrient(RepositoryTestCase):
    """Test the insert_global_nutrient method of the Repository class."""

    def test_insert_global_nutrient_inserts_nutrient(self):
        """Test that the method inserts a global nutrient into the database."""
        nutrient_name = 'test_nutrient'
        parent_id = 3
        # Check the nutrient name is not in the database
        all_nutrients = self.repository.fetch_all_global_nutrients()
        for nutrient_id, nutrient_data in all_nutrients.items():
            self.assertNotEqual(nutrient_data["nutrient_name"], nutrient_name)
        # Insert the nutrient
        id = self.repository.insert_global_nutrient(
            name=nutrient_name,
            parent_id=3,
        )
        # Fetch all the nutrients again
        all_nutrients = self.repository.fetch_all_global_nutrients()
        # Check the nutrient name is in the database
        name_in_db = False
        for nutrient_id, nutrient_data in all_nutrients.items():
            if nutrient_data["nutrient_name"] == nutrient_name:
                name_in_db = True
                assert id == nutrient_id # Check the ID was set correctly
                break
        self.assertTrue(name_in_db)
        # Check the parent_id is correct
        self.assertEqual(all_nutrients[id]["parent_id"], parent_id)

class TestInsertNutrientAlias(RepositoryTestCase):
    """Test the insert_nutrient_alias method of the Repository class."""

    def test_insert_nutrient_alias_inserts_alias(self):
        """Test that the method inserts a nutrient alias into the database."""
        nutrient_name = 'test_nutrient'
        alias = 'test_alias'
        # Assert the nutrient name is not in the database
        all_nutrients = self.repository.fetch_all_global_nutrients()
        for nutrient_id, nutrient_data in all_nutrients.items():
            self.assertNotEqual(nutrient_data["nutrient_name"], nutrient_name)
        # Insert the nutrient
        id = self.repository.insert_global_nutrient(
            name=nutrient_name,
            parent_id=3,
        )
        # Insert the alias
        self.repository.insert_nutrient_alias(
            primary_nutrient_id=id,
            alias=alias,
        )
        # Fetch all the nutrients again
        all_nutrients = self.repository.fetch_all_global_nutrients()
        # Check the alias listed against the nutrient
        assert alias in all_nutrients[id]["aliases"]

class TestInsertIngredientName(RepositoryTestCase):
    """Test the insert_ingredient_name method of the Repository class."""

    def test_insert_ingredient_name_inserts_name(self):
        """Test that the method inserts an ingredient name into the database."""
        ingredient_name = 'test_ingredient'
        # Assert the ingredient name is not in the database
        all_ingredient_names = self.repository.fetch_all_ingredient_names()
        for ingredient_name in all_ingredient_names:
            self.assertNotIn(ingredient_name, all_ingredient_names)
        # Insert the ingredient
        id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Fetch all the ingredients again
        all_ingredient_names = self.repository.fetch_all_ingredient_names()
        # Check the ingredient name is in the database
        self.assertIn(ingredient_name, all_ingredient_names)

class TestInsertIngredientNutrientQuantity(RepositoryTestCase):
    """Test the insert_ingredient_nutrient_quantity method of the Repository class."""

    def test_insert_ingredient_nutrient_quantity_inserts_nutrient_quantity(self):
        """Test that the method inserts an ingredient nutrient quantity into the database."""
        ingredient_name = 'test_ingredient'
        nutrient_name = 'test_nutrient'
        # Insert the ingredient
        ingredient_id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Insert the nutrient
        nutrient_id = self.repository.insert_global_nutrient(
            name=nutrient_name,
            parent_id=3,
        )
        # Check there are no nutrients on the ingredient yet
        ingredient_nutrients = self.repository.fetch_ingredient_nutrient_quantities(ingredient_id)
        self.assertNotIn(nutrient_id, ingredient_nutrients)
        # Insert the nutrient quantity
        self.repository.insert_ingredient_nutrient_quantity(
            ingredient_id=ingredient_id,
            nutrient_id=nutrient_id
        )
        # Fetch the ingredient nutrients again
        ingredient_nutrients = self.repository.fetch_ingredient_nutrient_quantities(ingredient_id)
        # Check the nutrient is in the ingredient
        self.assertIn(nutrient_id, ingredient_nutrients)
        # Assert there is only one nutrient in the ingredient
        self.assertEqual(len(ingredient_nutrients), 1)

class TestInsertRecipeName(RepositoryTestCase):
    """Test the insert_recipe_name method of the Repository class."""

    def test_insert_recipe_name_inserts_name(self):
        """Test that the method inserts a recipe name into the database."""
        recipe_name = 'test_recipe'
        # Assert the recipe name is not in the database
        all_recipe_names = self.repository.fetch_all_recipe_names()
        for recipe_name in all_recipe_names:
            self.assertNotIn(recipe_name, all_recipe_names)
        # Insert the recipe
        id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Fetch all the recipes again
        all_recipe_names = self.repository.fetch_all_recipe_names()
        # Check the recipe name is in the database
        self.assertIn(recipe_name, all_recipe_names)

class TestInsertGlobalRecipeTag(RepositoryTestCase):
    """Test the insert_global_recipe_tag method of the Repository class."""

    def test_insert_global_recipe_tag_inserts_tag(self):
        """Test that the method inserts a global recipe tag into the database."""
        tag_name = 'test_tag'
        # Assert the tag name is not in the database
        all_tags = self.repository.fetch_all_global_recipe_tags()
        for tag_id, tag_data in all_tags.items():
            self.assertNotEqual(tag_data["tag_name"], tag_name)
        # Insert the tag
        id = self.repository.insert_global_recipe_tag(
            name=tag_name,
        )
        # Fetch all the tags again
        all_tags = self.repository.fetch_all_global_recipe_tags()
        # Check the tag name is in the database
        name_in_db = False
        for tag_id, tag_data in all_tags.items():
            if tag_data["tag_name"] == tag_name:
                name_in_db = True
                assert id == tag_id # Check the ID was set correctly
                break
        self.assertTrue(name_in_db)
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

class TestInsertGlobalRecipeTag(RepositoryTestCase):
    """Test the insert_global_recipe_tag method of the Repository class."""

    def test_insert_global_recipe_tag_inserts_tag(self):
        """Test that the method inserts a global recipe tag into the database."""
        tag_name = 'test_tag'
        # Assert the tag name is not in the database
        all_tags = self.repository.fetch_all_global_recipe_tags()
        self.assertNotIn(tag_name, all_tags)
        # Insert the tag
        id = self.repository.insert_global_recipe_tag(
            tag_name=tag_name,
        )
        # Fetch all the tags again
        all_tags = self.repository.fetch_all_global_recipe_tags()
        # Check the tag name is in the database
        self.assertIn(tag_name, all_tags)

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

class TestInsertRecipeServeTimeWindow(RepositoryTestCase):
    """Test the insert_recipe_serve_time_window method of the Repository class."""

    def test_insert_recipe_serve_time_inserts_serve_time_window(self):
        """Test that the method inserts a recipe serve time into the database."""
        recipe_name = 'test_recipe'
        serve_time_window = "06:00 - 10:00"
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Check There are currently no serve times
        serve_time_windows = self.repository.fetch_recipe_serve_time_windows(
            recipe_id=recipe_id,
        )
        self.assertEqual(len(serve_time_windows), 0)
        # Insert the serve time
        serve_time_id = self.repository.insert_recipe_serve_time_window(
            recipe_id=recipe_id,
            serve_time_window=serve_time_window,
        )
        # Fetch the recipe serve time again
        serve_time_windows = self.repository.fetch_recipe_serve_time_windows(
            recipe_id=recipe_id,
        )
        # Check the new recipe serve time is in the database
        self.assertIn(serve_time_id, serve_time_windows.keys())
        # Check the new recipe serve time is correct
        self.assertEqual(serve_time_windows[serve_time_id], serve_time_window)

class TestUpdateIngredientName(RepositoryTestCase):
    """Test the update_ingredient_name method of the Repository class."""

    def test_update_ingredient_name_updates_name(self):
        """Test that the method updates an ingredient name in the database."""
        ingredient_name = 'test_ingredient'
        new_ingredient_name = 'new_test_ingredient'
        # Insert the ingredient
        id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Check the name is in the database
        all_ingredient_names = self.repository.fetch_all_ingredient_names()
        self.assertIn(ingredient_name, all_ingredient_names)
        # Update the ingredient name
        self.repository.update_ingredient_name(
            ingredient_id=id,
            name=new_ingredient_name,
        )
        # Fetch all the ingredients again
        all_ingredient_names = self.repository.fetch_all_ingredient_names()
        # Check the new ingredient name is in the database
        self.assertIn(new_ingredient_name, all_ingredient_names)
        # Check the old ingredient name is not in the database
        self.assertNotIn(ingredient_name, all_ingredient_names)

class TestUpdateIngredientDescription(RepositoryTestCase):
    """Test the update_ingredient_description method of the Repository class."""

    def test_update_ingredient_description_updates_description(self):
        """Test that the method updates an ingredient description in the database."""
        ingredient_name = 'test_ingredient'
        description_1 = 'test_description'
        description_2 = 'new_test_description'
        # Insert the ingredient
        id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Check the description is none
        description = self.repository.fetch_ingredient_description(id)
        self.assertIsNone(description)
        # Update the ingredient description
        self.repository.update_ingredient_description(
            ingredient_id=id,
            description=description_1,
        )
        # Fetch the ingredient description again
        description = self.repository.fetch_ingredient_description(id)
        # Check the new ingredient description is in the database
        self.assertEqual(description, description_1)
        # Update the ingredient description again
        self.repository.update_ingredient_description(
            ingredient_id=id,
            description=description_2,
        )
        # Fetch the ingredient description again
        description = self.repository.fetch_ingredient_description(id)
        # Check the new ingredient description is in the database
        self.assertEqual(description, description_2)

class TestUpdateIngredientCost(RepositoryTestCase):
    """Test the update_ingredient_cost method of the Repository class."""

    def test_update_ingredient_cost_updates_cost(self):
        """Test that the method updates an ingredient cost in the database."""
        ingredient_name = 'test_ingredient'
        cost_value = 2.50
        cost_qty_value = 100
        # Create a unit
        g_id = self.repository.insert_global_unit(
            unit_name='gram',
            plural_name='grams',
            unit_type='mass',
            aliases=['g'],
        )
        # Insert the ingredient
        ingredient_id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Check the cost is none
        cost = self.repository.fetch_ingredient_cost(ingredient_id)
        self.assertIsNone(cost["cost_value"])
        self.assertIsNone(cost["cost_qty_unit_id"])
        self.assertIsNone(cost["cost_qty_value"])
        # Update the ingredient cost
        self.repository.update_ingredient_cost(
            ingredient_id=ingredient_id,
            cost_value=cost_value,
            cost_qty_unit_id=g_id,
            cost_qty_value=cost_qty_value,
        )
        # Fetch the ingredient cost again
        cost = self.repository.fetch_ingredient_cost(ingredient_id)
        # Check the new ingredient cost is in the database
        self.assertEqual(cost["cost_value"], cost_value)
        self.assertEqual(cost["cost_qty_unit_id"], g_id)
        self.assertEqual(cost["cost_qty_value"], cost_qty_value)

class TestUpdateIngredientFlag(RepositoryTestCase):
    """Test the update_ingredient_flag method of the Repository class."""

    def test_update_ingredient_flag_updates_flag(self):
        """Test that the method updates an ingredient flag in the database."""
        ingredient_name = 'test_ingredient'
        flag_name = 'test_flag'
        # Insert the ingredient
        ingredient_id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Insert the flag
        flag_id = self.repository.insert_global_flag(flag_name)
        # Check the flag is not on the ingredient
        flags = self.repository.fetch_ingredient_flags(ingredient_id)
        self.assertNotIn(flag_id, flags)
        # Update the ingredient flag
        self.repository.upsert_ingredient_flag(
            ingredient_id=ingredient_id,
            flag_id=flag_id,
            value=True,
        )
        # Fetch the ingredient flags again
        flags = self.repository.fetch_ingredient_flags(ingredient_id)
        self.repository.connection.commit()
        # Check the flag is on the ingredient
        self.assertIn(flag_id, flags)
        # Check the flag value is True
        self.assertTrue(flags[flag_id])
        # Update the ingredient flag again
        self.repository.upsert_ingredient_flag(
            ingredient_id=ingredient_id,
            flag_id=flag_id,
            value=False,
        )
        # Fetch the ingredient flags again
        flags = self.repository.fetch_ingredient_flags(ingredient_id)
        # Check the flag value is False
        self.assertFalse(flags[flag_id])
        # Update the flag to None
        self.repository.upsert_ingredient_flag(
            ingredient_id=ingredient_id,
            flag_id=flag_id,
            value=None,
        )
        # Fetch the ingredient flags again
        flags = self.repository.fetch_ingredient_flags(ingredient_id)
        # Check the flag value is None
        self.assertIsNone(flags[flag_id])

class TestUpdateIngredientGI(RepositoryTestCase):
    """Test the update_ingredient_gi method of the Repository class."""

    def test_update_ingredient_gi_updates_gi(self):
        """Test that the method updates an ingredient GI in the database."""
        ingredient_name = 'test_ingredient'
        gi = 50
        # Insert the ingredient
        ingredient_id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Check the GI is none
        gi_in_db = self.repository.fetch_ingredient_gi(ingredient_id)
        self.assertIsNone(gi_in_db)
        # Update the ingredient GI
        self.repository.update_ingredient_gi(
            ingredient_id=ingredient_id,
            gi=gi,
        )
        # Fetch the ingredient GI again
        gi_in_db = self.repository.fetch_ingredient_gi(ingredient_id)
        # Check the new ingredient GI is in the database
        self.assertEqual(gi_in_db, gi)

class TestUpdateIngredientNutrientQuantity(RepositoryTestCase):
    """Test the update_ingredient_nutrient_quantity method of the Repository class."""

    def test_update_ingredient_nutrient_quantity_updates_nutrient_quantity(self):
        """Test that the method updates an ingredient nutrient quantity in the database."""
        ingredient_name = 'test_ingredient'
        nutrient_name = 'test_nutrient'
        nutrient_mass_value = 5
        ingredient_qty_value = 100
        # Insert the unit
        g_id = self.repository.insert_global_unit(
            unit_name='gram',
            plural_name='grams',
            unit_type='mass',
            aliases=['g'],
        )
        # Insert the ingredient
        ingredient_id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Insert the nutrient
        nutrient_id = self.repository.insert_global_nutrient(
            name=nutrient_name,
            parent_id=3,
        )
        # Check the nutrient is not on the ingredient
        nutrients = self.repository.fetch_ingredient_nutrient_quantities(ingredient_id)
        self.assertNotIn(nutrient_id, nutrients.keys())
        # Add the nutrient to the ingredient
        self.repository.upsert_ingredient_nutrient_quantity(
            ingredient_id=ingredient_id,
            global_nutrient_id=nutrient_id,
            ntr_mass_unit_id=g_id,
            ntr_mass_value=nutrient_mass_value,
            ing_qty_unit_id=g_id,
            ing_qty_value=ingredient_qty_value,
        )
        # Fetch the ingredient nutrients again
        nutrients = self.repository.fetch_ingredient_nutrient_quantities(ingredient_id)
        # Check the nutrient is on the ingredient
        self.assertIn(nutrient_id, nutrients.keys())
        # Check the nutrient mass value is correct
        self.assertEqual(nutrients[nutrient_id]["ntr_mass_value"], nutrient_mass_value)
        # Check the ingredient quantity value is correct
        self.assertEqual(nutrients[nutrient_id]["ing_qty_value"], ingredient_qty_value)
        # Check the nutrient mass unit is correct
        self.assertEqual(nutrients[nutrient_id]["ntr_mass_unit_id"], g_id)
        # Check the ingredient quantity unit is correct
        self.assertEqual(nutrients[nutrient_id]["ing_qty_unit_id"], g_id)

class TestUpdateRecipeName(RepositoryTestCase):
    """Test the update_recipe_name method of the Repository class."""

    def test_update_recipe_name_updates_name(self):
        """Test that the method updates a recipe name in the database."""
        recipe_name = 'test_recipe'
        new_recipe_name = 'new_test_recipe'
        # Check the name is not in the database
        recipe_names = self.repository.fetch_all_recipe_names()
        self.assertNotIn(recipe_name, recipe_names)
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Check the name is in the database
        all_recipe_names = self.repository.fetch_all_recipe_names()
        self.assertIn(recipe_name, all_recipe_names)
        # Update the recipe name
        self.repository.update_recipe_name(
            recipe_id=recipe_id,
            name=new_recipe_name,
        )
        # Fetch all the recipes again
        all_recipe_names = self.repository.fetch_all_recipe_names()
        # Check the new recipe name is in the database
        self.assertIn(new_recipe_name, all_recipe_names)
        # Check the old recipe name is not in the database
        self.assertNotIn(recipe_name, all_recipe_names)

class TestUpdateRecipeDescription(RepositoryTestCase):
    """Test the update_recipe_description method of the Repository class."""

    def test_update_recipe_description_updates_description(self):
        """Test that the method updates a recipe description in the database."""
        recipe_name = 'test_recipe'
        description_1 = 'test_description'
        description_2 = 'new_test_description'
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Check the description is none
        description = self.repository.fetch_recipe_description(recipe_id)
        self.assertIsNone(description)
        # Update the recipe description
        self.repository.update_recipe_description(
            recipe_id=recipe_id,
            description=description_1,
        )
        # Fetch the recipe description again
        description = self.repository.fetch_recipe_description(recipe_id)
        # Check the new recipe description is in the database
        self.assertEqual(description, description_1)
        # Update the recipe description again
        self.repository.update_recipe_description(
            recipe_id=recipe_id,
            description=description_2,
        )
        # Fetch the recipe description again
        description = self.repository.fetch_recipe_description(recipe_id)
        # Check the new recipe description is in the database
        self.assertEqual(description, description_2)

class TestRecipeInstructions(RepositoryTestCase):
    """Test the recipe_instructions method of the Repository class."""

    def test_recipe_instructions_updates_instructions(self):
        """Test that the method updates a recipe instructions in the database."""
        recipe_name = 'test_recipe'
        instructions_1 = 'test_instructions'
        instructions_2 = 'new_test_instructions'
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Check the instructions are none
        instructions = self.repository.fetch_recipe_instructions(recipe_id)
        self.assertIsNone(instructions)
        # Update the recipe instructions
        self.repository.update_recipe_instructions(
            recipe_id=recipe_id,
            instructions=instructions_1,
        )
        # Fetch the recipe instructions again
        instructions = self.repository.fetch_recipe_instructions(recipe_id)
        # Check the new recipe instructions are in the database
        self.assertEqual(instructions, instructions_1)
        # Update the recipe instructions again
        self.repository.update_recipe_instructions(
            recipe_id=recipe_id,
            instructions=instructions_2,
        )
        # Fetch the recipe instructions again
        instructions = self.repository.fetch_recipe_instructions(recipe_id)
        # Check the new recipe instructions are in the database
        self.assertEqual(instructions, instructions_2)

class TestUpdateRecipeIngredient(RepositoryTestCase):
    """Test the update_recipe_ingredient method of the Repository class."""

    def test_update_recipe_ingredient_updates_ingredient(self):
        """Test that the method updates a recipe ingredient in the database."""
        recipe_name = 'test_recipe'
        ingredient_name = 'test_ingredient'
        ingredient_qty_value = 100
        ingredient_qty_utol = 0.1
        ingredient_qty_ltol = 0.2
        # Insert the unit
        g_id = self.repository.insert_global_unit(
            unit_name='gram',
            plural_name='grams',
            unit_type='mass',
            aliases=['g'],
        )
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Insert the ingredient
        ingredient_id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Check the ingredient is not in the recipe
        ingredients = self.repository.fetch_recipe_ingredients(recipe_id)
        self.assertNotIn(ingredient_id, ingredients.keys())
        # Add the ingredient to the recipe
        self.repository.upsert_recipe_ingredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            qty_unit_id=g_id,
            qty_value=ingredient_qty_value,
            qty_utol=ingredient_qty_utol,
            qty_ltol=ingredient_qty_ltol,
        )
        # Fetch the recipe ingredients again
        ingredients = self.repository.fetch_recipe_ingredients(recipe_id)
        # Check the ingredient is in the recipe
        self.assertIn(ingredient_id, ingredients.keys())
        # Check the ingredient quantity value is correct
        self.assertEqual(ingredients[ingredient_id]["qty_value"], ingredient_qty_value)
        # Check the ingredient quantity unit is correct
        self.assertEqual(ingredients[ingredient_id]["qty_unit_id"], g_id)

class TestUpdateRecipeServeTimeWindow(RepositoryTestCase):
    """Test the update_recipe_serve_time_window method of the Repository class."""

    def test_update_recipe_serve_time_updates_serve_time_window(self):
        """Test that the method updates a recipe serve time in the database."""
        recipe_name = 'test_recipe'
        serve_time_window_1 = "06:00 - 10:00"
        serve_time_window_2 = "12:00 - 16:00"
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Insert the serve time
        serve_time_id = self.repository.insert_recipe_serve_time_window(
            recipe_id=recipe_id,
            serve_time_window=serve_time_window_1,
        )
        # Fetch the recipe serve time again
        serve_time_windows = self.repository.fetch_recipe_serve_time_windows(
            recipe_id=recipe_id,
        )
        # Check the new recipe serve time is in the database
        self.assertIn(serve_time_id, serve_time_windows.keys())
        # Check the new recipe serve time is correct
        self.assertEqual(serve_time_windows[serve_time_id], serve_time_window_1)
        # Update the serve time
        self.repository.update_recipe_serve_time_window(
            serve_time_id=serve_time_id,
            serve_time_window=serve_time_window_2,
        )
        # Fetch the recipe serve time again
        serve_time_windows = self.repository.fetch_recipe_serve_time_windows(
            recipe_id=recipe_id,
        )
        # Check the new recipe serve time is in the database
        self.assertIn(serve_time_id, serve_time_windows.keys())
        # Check the new recipe serve time is correct
        self.assertEqual(serve_time_windows[serve_time_id], serve_time_window_2)
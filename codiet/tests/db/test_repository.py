from . import DatabaseTestCase


class TestInsertGlobalUnit(DatabaseTestCase):
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
        # Assert the aliases are correct
        # Grab the alias IDs
        alias_ids = self.repository.fetch_global_unit_aliases(g_id)
        # Find the alias ID where the string is 'g'
        g_alias_id = None
        for alias_id, alias in alias_ids.items():
            if alias == 'g':
                g_alias_id = alias_id
                break
        # Find the alias ID where the string is 'kg'
        kg_alias_id = None
        alias_ids = self.repository.fetch_global_unit_aliases(kg_id)
        for alias_id, alias in alias_ids.items():
            if alias == 'kg':
                kg_alias_id = alias_id
                break
        # Assert the g alias is there
        self.assertIn(g_alias_id, global_units[g_id]["aliases"].keys())
        self.assertEqual(global_units[g_id]["aliases"][g_alias_id], 'g')
        # Assert the kg alias is there
        self.assertIn(kg_alias_id, global_units[kg_id]["aliases"].keys())
        self.assertEqual(global_units[kg_id]["aliases"][kg_alias_id], 'kg')
        # Assert the conversions are there
        # Check there is a conversion for g_id in kg conversions
        self.assertIn(g_id, global_units[kg_id]["conversions"])
        # Check the conversion is correct
        self.assertEqual(global_units[kg_id]["conversions"][g_id], 1000)

class TestInsertGlobalFlag(DatabaseTestCase):
    """Test the insert_global_flag method of the Repository class."""

    def test_insert_global_flag_inserts_flag(self):
        """Test that the method inserts a global flag into the database."""
        flag_name = 'test_flag'
        # Insert the flag
        flag_id = self.repository.insert_global_flag(flag_name)
        # Fetch all the flags
        flags = self.repository.fetch_all_global_flags()
        # Check the flag ID is in the keys
        self.assertIn(flag_id, flags.keys())
        # Check the flag name is under the correct key
        self.assertEqual(flags[flag_id], flag_name)

class TestInsertGlobalNutrient(DatabaseTestCase):
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

class TestInsertNutrientAlias(DatabaseTestCase):
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

class TestInsertGlobalRecipeTag(DatabaseTestCase):
    """Test the insert_global_recipe_tag method of the Repository class."""

    def test_insert_global_recipe_tag_inserts_tag(self):
        """Test that the method inserts a global recipe tag into the database."""
        tag_name = 'test_tag'
        # Fetch all the tags
        all_tags = self.repository.fetch_all_global_recipe_tags()
        # Assert there are no tags yet
        self.assertEqual(len(all_tags), 0)
        # Insert the tag
        tag_id = self.repository.insert_global_recipe_tag(tag_name)
        # Fetch all the tags again
        all_tags = self.repository.fetch_all_global_recipe_tags()
        # Check the tag ID is in the keys
        self.assertIn(tag_id, all_tags.keys())
        # Check the tag name is under the correct key
        self.assertEqual(all_tags[tag_id], tag_name)

class TestInsertIngredientName(DatabaseTestCase):
    """Test the insert_ingredient_name method of the Repository class."""

    def test_insert_ingredient_name_inserts_name(self):
        """Test that the method inserts an ingredient name into the database."""
        ingredient_name = 'test_ingredient'
        # Assert there are no ingredient names in the database
        all_ingredients = self.repository.fetch_all_ingredient_names()
        self.assertEqual(len(all_ingredients), 0)
        # Insert the ingredient
        ingredient_id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Fetch all the ingredients again
        all_ingredients = self.repository.fetch_all_ingredient_names()
        # Check the ingredient name is in the database
        self.assertIn(ingredient_id, all_ingredients.keys())
        # Check the ingredient name is correct
        self.assertEqual(all_ingredients[ingredient_id], ingredient_name)

class TestInsertIngredientUnit(DatabaseTestCase):
    """Test the insert_ingredient_unit method of the Repository class."""

    def test_insert_ingredient_unit_inserts_unit(self):
        """Test that the method inserts an ingredient unit into the database."""
        ingredient_name = 'test_ingredient'
        # Insert the ingredient
        ingredient_id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Define the unit
        unit_name = 'lb'
        plural_name = 'lbs'
        unit_type = 'mass'
        ref_unit_name = 'g'
        ref_plural_name = 'g'
        ref_unit_type = 'mass'
        # Insert the global unit
        unit_global_id = self.repository.insert_global_unit(
            unit_name=unit_name,
            plural_name=plural_name,
            unit_type=unit_type,
        )
        # Insert the reference global unit
        ref_unit_global_id = self.repository.insert_global_unit(
            unit_name=ref_unit_name,
            plural_name=ref_plural_name,
            unit_type=ref_unit_type,
        )
        # Insert the ingredient unit
        ingredient_unit_id = self.repository.insert_ingredient_unit(
            ingredient_id=ingredient_id,
            unit_global_id=unit_global_id,
            ref_unit_global_id=ref_unit_global_id,
            unit_qty=1,
            ref_unit_qty=2,
        )
        # Fetch the ingredient units
        ingredient_units = self.repository.fetch_ingredient_units(ingredient_id)
        # Check the new unit is in the database
        self.assertIn(ingredient_unit_id, ingredient_units.keys())
        # Assert the unit global ID is set correctly
        self.assertEqual(ingredient_units[ingredient_unit_id]["unit_global_id"], unit_global_id)
        # Assert the ref unit global ID is set correctly
        self.assertEqual(ingredient_units[ingredient_unit_id]["ref_unit_global_id"], ref_unit_global_id)
        # Assert the unit qty is set correctly
        self.assertEqual(ingredient_units[ingredient_unit_id]["unit_qty"], 1)
        # Assert the ref unit qty is set correctly
        self.assertEqual(ingredient_units[ingredient_unit_id]["ref_unit_qty"], 2)

class TestInsertRecipeName(DatabaseTestCase):
    """Test the insert_recipe_name method of the Repository class."""

    def test_insert_recipe_name_inserts_name(self):
        """Test that the method inserts a recipe name into the database."""
        recipe_name = 'test_recipe'
        # Assert there are no recipe names in the database
        all_recipes = self.repository.fetch_all_recipe_names()
        self.assertEqual(len(all_recipes), 0)
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Fetch all the recipes again
        all_recipes = self.repository.fetch_all_recipe_names()
        # Check the recipe name is in the database
        self.assertIn(recipe_id, all_recipes.keys())
        # Check the recipe name is correct
        self.assertEqual(all_recipes[recipe_id], recipe_name)

class TestInsertRecipeServeTimeWindow(DatabaseTestCase):
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

class TestUpdateIngredientName(DatabaseTestCase):
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
        all_ingredients = self.repository.fetch_all_ingredient_names()
        self.assertIn(id, all_ingredients.keys())
        # Check the name is correct
        self.assertEqual(all_ingredients[id], ingredient_name)
        # Update the ingredient name
        self.repository.update_ingredient_name(
            ingredient_id=id,
            name=new_ingredient_name,
        )
        # Fetch all the ingredients again
        all_ingredients = self.repository.fetch_all_ingredient_names()
        # Check the new ingredient name is in the database
        self.assertIn(id, all_ingredients.keys())
        # Check the old ingredient name is not in the database
        self.assertNotIn(ingredient_name, all_ingredients.values())
        # Check the new ingredient name is correct
        self.assertEqual(all_ingredients[id], new_ingredient_name)

class TestUpdateIngredientDescription(DatabaseTestCase):
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

class TestUpdateIngredientUnit(DatabaseTestCase):
    """Test the update_ingredient_unit method of the Repository class."""

    def test_update_ingredient_unit_updates_unit(self):
        """Test that the method updates an ingredient unit in the database."""
        ingredient_name = 'test_ingredient'
        unit_name = 'lb'
        plural_name = 'lbs'
        unit_type = 'mass'
        ref_unit_name = 'g'
        ref_plural_name = 'g'
        ref_unit_type = 'mass'
        unit_qty = 1
        ref_unit_qty = 2
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
        # Insert the unit
        unit_id = self.repository.insert_global_unit(
            unit_name=unit_name,
            plural_name=plural_name,
            unit_type=unit_type,
        )
        # Insert the reference unit
        ref_unit_id = self.repository.insert_global_unit(
            unit_name=ref_unit_name,
            plural_name=ref_plural_name,
            unit_type=ref_unit_type,
        )
        # Insert the ingredient unit
        ingredient_unit_id = self.repository.insert_ingredient_unit(
            ingredient_id=ingredient_id,
            unit_global_id=unit_id,
            ref_unit_global_id=ref_unit_id,
            unit_qty=unit_qty,
            ref_unit_qty=ref_unit_qty,
        )
        # Fetch the ingredient units
        ingredient_units = self.repository.fetch_ingredient_units(ingredient_id)
        # Check the new unit is in the database
        self.assertIn(ingredient_unit_id, ingredient_units.keys())
        # Update the ingredient unit
        self.repository.update_ingredient_unit(
            ingredient_unit_id=ingredient_unit_id,
            unit_global_id=g_id,
            ref_unit_global_id=g_id,
            unit_qty=1,
            ref_unit_qty=1,
        )
        # Fetch the ingredient units again
        ingredient_units = self.repository.fetch_ingredient_units(ingredient_id)
        # Check the new unit is in the database
        self.assertIn(ingredient_unit_id, ingredient_units.keys())
        # Check the unit global ID is correct
        self.assertEqual(ingredient_units[ingredient_unit_id]["unit_global_id"], g_id)
        # Check the ref unit global ID is correct
        self.assertEqual(ingredient_units[ingredient_unit_id]["ref_unit_global_id"], g_id)
        # Check the unit qty is correct
        self.assertEqual(ingredient_units[ingredient_unit_id]["unit_qty"], 1)
        # Check the ref unit qty is correct
        self.assertEqual(ingredient_units[ingredient_unit_id]["ref_unit_qty"], 1)       

class TestUpdateIngredientCost(DatabaseTestCase):
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

class TestUpdateIngredientFlag(DatabaseTestCase):
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

class TestUpdateIngredientGI(DatabaseTestCase):
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

class TestUpdateIngredientNutrientQuantity(DatabaseTestCase):
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

class TestUpdateRecipeName(DatabaseTestCase):
    """Test the update_recipe_name method of the Repository class."""

    def test_update_recipe_name_updates_name(self):
        """Test that the method updates a recipe name in the database."""
        recipe_name = 'test_recipe'
        new_recipe_name = 'new_test_recipe'
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Check the name is in the database
        all_recipes = self.repository.fetch_all_recipe_names()
        self.assertIn(recipe_id, all_recipes.keys())
        # Check the name is correct
        self.assertEqual(all_recipes[recipe_id], recipe_name)
        # Update the recipe name
        self.repository.update_recipe_name(
            recipe_id=recipe_id,
            name=new_recipe_name,
        )
        # Fetch all the recipes again
        all_recipes = self.repository.fetch_all_recipe_names()
        # Check the new recipe name is in the database
        self.assertIn(recipe_id, all_recipes.keys())
        # Check the old recipe name is not in the database
        self.assertNotIn(recipe_name, all_recipes.values())
        # Check the new recipe name is correct
        self.assertEqual(all_recipes[recipe_id], new_recipe_name)

class TestUpdateRecipeDescription(DatabaseTestCase):
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

class TestRecipeInstructions(DatabaseTestCase):
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

class TestUpdateRecipeIngredient(DatabaseTestCase):
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

class TestUpdateRecipeServeTimeWindow(DatabaseTestCase):
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

class TestUpdateRecipeTags(DatabaseTestCase):
    """Test the update_recipe_tags method of the Repository class."""

    def test_update_recipe_tags_updates_tags(self):
        """Test that the method updates a recipe tags in the database."""
        recipe_name = 'test_recipe'
        tag_1 = 'test_tag_1'
        tag_2 = 'test_tag_2'
        tag_3 = 'test_tag_3'
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Insert the global tags
        tag_id_1 = self.repository.insert_global_recipe_tag(tag_1)
        tag_id_2 = self.repository.insert_global_recipe_tag(tag_2)
        tag_id_3 = self.repository.insert_global_recipe_tag(tag_3)
        # Attach tags 1 and 2 to the recipe
        self.repository.update_recipe_tags(
            recipe_id=recipe_id,
            recipe_tag_ids=[tag_id_1, tag_id_2],
        )
        # Check the tags went into the recipe
        recipe_tags = self.repository.fetch_recipe_tags(recipe_id)
        self.assertEqual(len(recipe_tags), 2)
        # Check both tag ID's are in the list
        self.assertIn(tag_id_1, recipe_tags)
        self.assertIn(tag_id_2, recipe_tags)
        # Update the tags to 2 and 3
        self.repository.update_recipe_tags(
            recipe_id=recipe_id,
            recipe_tag_ids=[tag_id_2, tag_id_3],
        )
        # Check the tags went into the recipe
        recipe_tags = self.repository.fetch_recipe_tags(recipe_id)
        self.assertEqual(len(recipe_tags), 2)
        # Check both tag ID's are in the list
        self.assertIn(tag_id_2, recipe_tags)
        self.assertIn(tag_id_3, recipe_tags)

class TestDeleteIngredient(DatabaseTestCase):
    """Test the delete_ingredient method of the Repository class."""

    def test_delete_ingredient_deletes_ingredient(self):
        """Test that the method deletes an ingredient in the database."""
        ingredient_name = 'test_ingredient'
        # Insert the ingredient
        ingredient_id = self.repository.insert_ingredient_name(
            name=ingredient_name,
        )
        # Check the ingredient is in the database
        all_ingredients = self.repository.fetch_all_ingredient_names()
        self.assertIn(ingredient_id, all_ingredients.keys())
        # Delete the ingredient
        self.repository.delete_ingredient(ingredient_id)
        # Fetch all the ingredients again
        all_ingredients = self.repository.fetch_all_ingredient_names()
        # Check the ingredient is not in the database
        self.assertNotIn(ingredient_id, all_ingredients.keys())

class TestDeleteRecipe(DatabaseTestCase):
    """Test the delete_recipe method of the Repository class."""

    def test_delete_recipe_deletes_recipe(self):
        """Test that the method deletes a recipe in the database."""
        recipe_name = 'test_recipe'
        # Insert the recipe
        recipe_id = self.repository.insert_recipe_name(
            name=recipe_name,
        )
        # Check the recipe is in the database
        all_recipes = self.repository.fetch_all_recipe_names()
        self.assertIn(recipe_id, all_recipes.keys())
        # Delete the recipe
        self.repository.delete_recipe(recipe_id)
        # Fetch all the recipes again
        all_recipes = self.repository.fetch_all_recipe_names()
        # Check the recipe is not in the database
        self.assertNotIn(recipe_id, all_recipes.keys())
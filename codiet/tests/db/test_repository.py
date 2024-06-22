from . import DatabaseTestCase


class TestCreateGlobalUnit(DatabaseTestCase):
    """Test the insert_global_unit method of the Repository class."""

    def test_create_global_unit_creates_unit(self):
        """Test that the method adds a global unit into the database."""
        # Create a gram measurement unit
        g_id = self.repository.create_global_unit(
            unit_name='gram',
            single_display_name='g',
            plural_display_name='gs',
            unit_type='mass',
            aliases=['grams'],
        )
        # Create a kg measurement unit
        kg_id = self.repository.create_global_unit(
            unit_name='kilogram',
            single_display_name='kg',
            plural_display_name='kgs',
            unit_type='mass',
            aliases=['kilograms']
        )
        # Check that both gram and kg units are in the database
        # Grab a list of global units
        global_units = self.repository.read_all_global_units()
        # Assert that the unit names are there
        self.assertEqual(global_units[g_id]["unit_name"], 'gram')
        self.assertEqual(global_units[kg_id]["unit_name"], 'kilogram')
        # Assert that the single display names are there
        self.assertEqual(global_units[g_id]["single_display_name"], 'g')
        self.assertEqual(global_units[kg_id]["single_display_name"], 'kg')
        # Assert that the plural display names are there
        self.assertEqual(global_units[g_id]["plural_display_name"], 'gs')
        self.assertEqual(global_units[kg_id]["plural_display_name"], 'kgs')
        # Assert the unit types are correct
        self.assertEqual(global_units[g_id]["unit_type"], 'mass')
        self.assertEqual(global_units[kg_id]["unit_type"], 'mass')
        # Assert the aliases are correct
        aliases = self.repository.read_global_unit_aliases(g_id)
        self.assertIn('grams', aliases.values())
        aliases = self.repository.read_global_unit_aliases(kg_id)
        self.assertIn('kilograms', aliases.values())

class TestCreateGlobalFlag(DatabaseTestCase):
    """Test the insert_global_flag method of the Repository class."""

    def test_insert_global_flag_inserts_flag(self):
        """Test that the method inserts a global flag into the database."""
        flag_name = 'test_flag'
        # Insert the flag
        flag_id = self.repository.create_global_flag(flag_name)
        # Fetch all the flags
        flags = self.repository.read_all_global_flags()
        # Check the flag ID is in the keys
        self.assertIn(flag_id, flags.keys())
        # Check the flag name is under the correct key
        self.assertEqual(flags[flag_id], flag_name)

class TestCreateGlobalNutrient(DatabaseTestCase):
    """Test the insert_global_nutrient method of the Repository class."""

    def test_insert_global_nutrient_inserts_nutrient(self):
        """Test that the method inserts a global nutrient into the database."""
        nutrient_name = 'test_nutrient'
        parent_id = 3
        # Check the nutrient name is not in the database
        all_nutrients = self.repository.read_all_global_nutrients()
        for nutrient_id, nutrient_data in all_nutrients.items():
            self.assertNotEqual(nutrient_data["nutrient_name"], nutrient_name)
        # Insert the nutrient
        id = self.repository.create_global_nutrient(
            name=nutrient_name,
            parent_id=3,
        )
        # Fetch all the nutrients again
        all_nutrients = self.repository.read_all_global_nutrients()
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

class TestCreateNutrientAlias(DatabaseTestCase):
    """Test the insert_nutrient_alias method of the Repository class."""

    def test_insert_nutrient_alias_inserts_alias(self):
        """Test that the method inserts a nutrient alias into the database."""
        nutrient_name = 'test_nutrient'
        alias = 'test_alias'
        # Assert the nutrient name is not in the database
        all_nutrients = self.repository.read_all_global_nutrients()
        for nutrient_id, nutrient_data in all_nutrients.items():
            self.assertNotEqual(nutrient_data["nutrient_name"], nutrient_name)
        # Insert the nutrient
        id = self.repository.create_global_nutrient(
            name=nutrient_name,
            parent_id=3,
        )
        # Insert the alias
        self.repository.create_nutrient_alias(
            primary_nutrient_id=id,
            alias=alias,
        )
        # Fetch all the nutrients again
        all_nutrients = self.repository.read_all_global_nutrients()
        # Check the alias listed against the nutrient
        assert alias in all_nutrients[id]["aliases"]

class TestCreateGlobalRecipeTag(DatabaseTestCase):
    """Test the insert_global_recipe_tag method of the Repository class."""

    def test_insert_global_recipe_tag_inserts_tag(self):
        """Test that the method inserts a global recipe tag into the database."""
        tag_name = 'test_tag'
        # Fetch all the tags
        all_tags = self.repository.read_all_global_recipe_tags()
        # Assert there are no tags yet
        self.assertEqual(len(all_tags), 0)
        # Insert the tag
        tag_id = self.repository.create_global_recipe_tag(tag_name)
        # Fetch all the tags again
        all_tags = self.repository.read_all_global_recipe_tags()
        # Check the tag ID is in the keys
        self.assertIn(tag_id, all_tags.keys())
        # Check the tag name is under the correct key
        self.assertEqual(all_tags[tag_id], tag_name)

class TestCreateIngredientName(DatabaseTestCase):
    """Test the insert_ingredient_name method of the Repository class."""

    def test_insert_ingredient_name_inserts_name(self):
        """Test that the method inserts an ingredient name into the database."""
        ingredient_name = 'test_ingredient'
        # Assert there are no ingredient names in the database
        all_ingredients = self.repository.read_all_ingredient_names()
        self.assertEqual(len(all_ingredients), 0)
        # Insert the ingredient
        ingredient_id = self.repository.create_ingredient_name(
            name=ingredient_name,
        )
        # Fetch all the ingredients again
        all_ingredients = self.repository.read_all_ingredient_names()
        # Check the ingredient name is in the database
        self.assertIn(ingredient_id, all_ingredients.keys())
        # Check the ingredient name is correct
        self.assertEqual(all_ingredients[ingredient_id], ingredient_name)

class TestCreateIngredientFlag(DatabaseTestCase):
    """Test the insert_ingredient_flag method of the Repository class."""

    def test_insert_ingredient_flag_inserts_flag(self):
        """Test that the method inserts an ingredient flag into the database."""
        ingredient_name = 'test_ingredient'
        flag_name = 'test_flag'
        # Insert the ingredient
        ingredient_id = self.repository.create_ingredient_name(
            name=ingredient_name,
        )
        # Insert the flag
        flag_id = self.repository.create_global_flag(flag_name)
        # Check the flag is not on the ingredient
        flags = self.repository.read_ingredient_flags(ingredient_id)
        self.assertNotIn(flag_id, flags)
        # Insert the flag on the ingredient
        ingredient_flag_id = self.repository.create_ingredient_flag(
            ingredient_id=ingredient_id,
            flag_id=flag_id,
            value=True,
        )
        # Fetch the ingredient flags again
        flags = self.repository.read_ingredient_flags(ingredient_id)
        # Check the flag is on the ingredient
        self.assertIn(ingredient_flag_id, flags)
        # Check the flag value is True
        self.assertTrue(flags[ingredient_flag_id])

class TestCreateIngredientUnitConversion(DatabaseTestCase):
    """Test the insert_ingredient_unit method of the Repository class."""

    def test_create_ingredient_unit_conversion_creates_ingredient_unit_conversion(self):
        """Test that the method inserts an ingredient unit into the database."""
        # Need to generate an ingredient ID, so create an ingredient
        ingredient_name = 'test_ingredient'
        ingredient_id = self.repository.create_ingredient_name(
            name=ingredient_name,
        )
        # Now create two units to convert between
        g_id = self.repository.create_global_unit(
            unit_name='gram',
            single_display_name='g',
            plural_display_name='g',
            unit_type='mass'
        )
        slice_id = self.repository.create_global_unit(
            unit_name='slice',
            single_display_name='slice',
            plural_display_name='slices',
            unit_type='group'
        )
        # Insert the ingredient unit conversion
        unit_conversion_id = self.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient_id,
            from_unit_id=g_id,
            to_unit_id=slice_id,
            from_unit_qty=100,
            to_unit_qty=1,
        )
        # Fetch the ingredient units
        ing_unit_conversions = self.repository.read_ingredient_unit_conversions(ingredient_id)
        # Check the new unit is in the database
        self.assertIn(unit_conversion_id, ing_unit_conversions.keys())
        # Assert the unit global ID is set correctly
        self.assertEqual(ing_unit_conversions[unit_conversion_id]["from_unit_id"], g_id)
        # Assert the ref unit global ID is set correctly
        self.assertEqual(ing_unit_conversions[unit_conversion_id]["to_unit_id"], slice_id)
        # Assert the unit qty is set correctly
        self.assertEqual(ing_unit_conversions[unit_conversion_id]["from_unit_qty"], 100)
        # Assert the ref unit qty is set correctly
        self.assertEqual(ing_unit_conversions[unit_conversion_id]["to_unit_qty"], 1)

class TestCreateRecipeName(DatabaseTestCase):
    """Test the insert_recipe_name method of the Repository class."""

    def test_insert_recipe_name_inserts_name(self):
        """Test that the method inserts a recipe name into the database."""
        recipe_name = 'test_recipe'
        # Assert there are no recipe names in the database
        all_recipes = self.repository.read_all_recipe_names()
        self.assertEqual(len(all_recipes), 0)
        # Insert the recipe
        recipe_id = self.repository.create_recipe_name(
            name=recipe_name,
        )
        # Fetch all the recipes again
        all_recipes = self.repository.read_all_recipe_names()
        # Check the recipe name is in the database
        self.assertIn(recipe_id, all_recipes.keys())
        # Check the recipe name is correct
        self.assertEqual(all_recipes[recipe_id], recipe_name)

class TestCreateRecipeIngredientQuantity(DatabaseTestCase):
    """Test the insert_recipe_ingredient method of the Repository class."""

    def test_create_recipe_ingredient_quantity_ingredient_quantity(self):
        """Test that the method inserts a recipe ingredient into the database."""
        # Insert the unit
        g_id = self.repository.create_global_unit(
            unit_name='gram',
            single_display_name='g',
            plural_display_name='g',
            unit_type='mass',
        )
        # Insert the recipe
        recipe_id = self.repository.create_recipe_name(
            name="Test Recipe",
        )
        # Insert the ingredient
        ingredient_id = self.repository.create_ingredient_name(
            name="Test Ingredient",
        )
        # Check there are no ingredients in the recipe
        ingredient_quantities = self.repository.read_recipe_ingredient_quantities(recipe_id)
        self.assertEqual(len(ingredient_quantities), 0)
        # Add the ingredient to the recipe
        ingredient_qty_id = self.repository.create_recipe_ingredient_quantity(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            qty_unit_id=g_id,
            qty_value=100,
            qty_utol=10,
            qty_ltol=15,
        )
        # Fetch the recipe ingredients again
        ingredient_quantities = self.repository.read_recipe_ingredient_quantities(recipe_id)
        # Check the ingredient is in the recipe
        self.assertIn(ingredient_qty_id, ingredient_quantities.keys())
        # Check the ingredient quantity value is correct
        self.assertEqual(ingredient_quantities[ingredient_id]["qty_value"], 100)
        # Check the ingredient quantity unit is correct
        self.assertEqual(ingredient_quantities[ingredient_id]["qty_unit_id"], g_id)
        # Check the ingredient quantity upper tolerance is correct
        self.assertEqual(ingredient_quantities[ingredient_id]["qty_utol"], 10)
        # Check the ingredient quantity lower tolerance is correct
        self.assertEqual(ingredient_quantities[ingredient_id]["qty_ltol"], 15)

class TestInsertRecipeServeTimeWindow(DatabaseTestCase):
    """Test the insert_recipe_serve_time_window method of the Repository class."""

    def test_insert_recipe_serve_time_inserts_serve_time_window(self):
        """Test that the method inserts a recipe serve time into the database."""
        recipe_name = 'test_recipe'
        serve_time_window = "06:00 - 10:00"
        # Insert the recipe
        recipe_id = self.repository.create_recipe_name(
            name=recipe_name,
        )
        # Check There are currently no serve times
        serve_time_windows = self.repository.read_recipe_serve_time_windows(
            recipe_id=recipe_id,
        )
        self.assertEqual(len(serve_time_windows), 0)
        # Insert the serve time
        serve_time_id = self.repository.create_recipe_serve_time_window(
            recipe_id=recipe_id,
            serve_time_window=serve_time_window,
        )
        # Fetch the recipe serve time again
        serve_time_windows = self.repository.read_recipe_serve_time_windows(
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
        id = self.repository.create_ingredient_name(
            name=ingredient_name,
        )
        # Check the name is in the database
        all_ingredients = self.repository.read_all_ingredient_names()
        self.assertIn(id, all_ingredients.keys())
        # Check the name is correct
        self.assertEqual(all_ingredients[id], ingredient_name)
        # Update the ingredient name
        self.repository.update_ingredient_name(
            ingredient_id=id,
            name=new_ingredient_name,
        )
        # Fetch all the ingredients again
        all_ingredients = self.repository.read_all_ingredient_names()
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
        id = self.repository.create_ingredient_name(
            name=ingredient_name,
        )
        # Check the description is none
        description = self.repository.read_ingredient_description(id)
        self.assertIsNone(description)
        # Update the ingredient description
        self.repository.update_ingredient_description(
            ingredient_id=id,
            description=description_1,
        )
        # Fetch the ingredient description again
        description = self.repository.read_ingredient_description(id)
        # Check the new ingredient description is in the database
        self.assertEqual(description, description_1)
        # Update the ingredient description again
        self.repository.update_ingredient_description(
            ingredient_id=id,
            description=description_2,
        )
        # Fetch the ingredient description again
        description = self.repository.read_ingredient_description(id)
        # Check the new ingredient description is in the database
        self.assertEqual(description, description_2)

class TestUpdateIngredientUnitConversion(DatabaseTestCase):
    """Test the update_ingredient_unit method of the Repository class."""

    def test_update_ingredient_unit_conversion_updates_unit_conversion(self):
        """Test that the method updates an ingredient unit in the database."""
        # Insert the unit first unit
        g_id = self.repository.create_global_unit(
            unit_name='gram',
            single_display_name='g',
            plural_display_name='g',
            unit_type='mass',
        )
        # Insert the second unit
        slice_id = self.repository.create_global_unit(
            unit_name='slice',
            single_display_name='slice',
            plural_display_name='slices',
            unit_type='collective',
        )
        # Insert the ingredient
        ingredient_id = self.repository.create_ingredient_name(
            name="Test Ingredient",
        )
        # Insert the ingredient unit conversion
        ingredient_unit_id = self.repository.create_ingredient_unit_conversion(
            ingredient_id=ingredient_id,
            from_unit_id=g_id,
            to_unit_id=slice_id,
            from_unit_qty=100,
            to_unit_qty=1,
        )
        # Fetch the ingredient unit conversions
        unit_conversions = self.repository.read_ingredient_unit_conversions(ingredient_id)
        # Check the new unit was saved
        self.assertIn(ingredient_unit_id, unit_conversions.keys())
        # Check the from unit ID is correct
        self.assertEqual(unit_conversions[ingredient_unit_id]["from_unit_id"], g_id)
        # Check the to unit ID is correct
        self.assertEqual(unit_conversions[ingredient_unit_id]["to_unit_id"], slice_id)
        # Check the from unit qty is correct
        self.assertEqual(unit_conversions[ingredient_unit_id]["from_unit_qty"], 100)
        # Check the to unit qty is correct
        self.assertEqual(unit_conversions[ingredient_unit_id]["to_unit_qty"], 1)
        # Update the ingredient unit
        self.repository.update_ingredient_unit_conversion(
            ingredient_unit_id=ingredient_unit_id,
            from_unit_id=g_id,
            to_unit_id=slice_id,
            from_unit_qty=100,
            to_unit_qty=2,
        )
        # Fetch the ingredient units again
        unit_conversions = self.repository.read_ingredient_unit_conversions(ingredient_id)
        # Check the new unit was saved
        self.assertIn(ingredient_unit_id, unit_conversions.keys())
        # Check the from unit ID is correct
        self.assertEqual(unit_conversions[ingredient_unit_id]["from_unit_id"], g_id)
        # Check the to unit ID is correct
        self.assertEqual(unit_conversions[ingredient_unit_id]["to_unit_id"], slice_id)
        # Check the from unit qty is correct
        self.assertEqual(unit_conversions[ingredient_unit_id]["from_unit_qty"], 100)
        # Check the to unit qty is correct
        self.assertEqual(unit_conversions[ingredient_unit_id]["to_unit_qty"], 2)

class TestUpdateIngredientCost(DatabaseTestCase):
    """Test the update_ingredient_cost method of the Repository class."""

    def test_update_ingredient_cost_updates_cost(self):
        """Test that the method updates an ingredient cost in the database."""
        ingredient_name = 'test_ingredient'
        cost_value = 2.50
        cost_qty_value = 100
        # Create a unit
        g_id = self.repository.create_global_unit(
            unit_name='gram',
            single_display_name='g',
            plural_display_name='g',
            unit_type='mass',
        )
        # Insert the ingredient
        ingredient_id = self.repository.create_ingredient_name(
            name=ingredient_name,
        )
        # Check the cost is none
        cost = self.repository.read_ingredient_cost(ingredient_id)
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
        cost = self.repository.read_ingredient_cost(ingredient_id)
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
        ingredient_id = self.repository.create_ingredient_name(
            name=ingredient_name,
        )
        # Insert the global flag
        flag_id = self.repository.create_global_flag(flag_name)
        # Set the global flag on the ingredient
        ingredient_flag_id = self.repository.create_ingredient_flag(
            ingredient_id=ingredient_id,
            flag_id=flag_id,
            value=True,
        )
        # Fetch the ingredient flags
        flags = self.repository.read_ingredient_flags(ingredient_id)
        # Check the flag is in the database
        self.assertIn(ingredient_flag_id, flags.keys())
        # Check the flag value is True
        self.assertTrue(flags[ingredient_flag_id])
        # Update the ingredient flag
        self.repository.update_ingredient_flag(
            ingredient_flag_id=ingredient_flag_id,
            value=False,
        )
        # Fetch the ingredient flags again
        flags = self.repository.read_ingredient_flags(ingredient_id)
        # Check the flag is in the database
        self.assertIn(ingredient_flag_id, flags.keys())
        # Check the flag value is False
        self.assertFalse(flags[ingredient_flag_id])

class TestUpdateIngredientGI(DatabaseTestCase):
    """Test the update_ingredient_gi method of the Repository class."""

    def test_update_ingredient_gi_updates_gi(self):
        """Test that the method updates an ingredient GI in the database."""
        ingredient_name = 'test_ingredient'
        gi = 50
        # Insert the ingredient
        ingredient_id = self.repository.create_ingredient_name(
            name=ingredient_name,
        )
        # Check the GI is none
        gi_in_db = self.repository.read_ingredient_gi(ingredient_id)
        self.assertIsNone(gi_in_db)
        # Update the ingredient GI
        self.repository.update_ingredient_gi(
            ingredient_id=ingredient_id,
            gi=gi,
        )
        # Fetch the ingredient GI again
        gi_in_db = self.repository.read_ingredient_gi(ingredient_id)
        # Check the new ingredient GI is in the database
        self.assertEqual(gi_in_db, gi)

class TestUpdateIngredientNutrientQuantity(DatabaseTestCase):
    """Test the update_ingredient_nutrient_quantity method of the Repository class."""

    def test_update_ingredient_nutrient_quantity_updates_nutrient_quantity(self):
        """Test that the method updates an ingredient nutrient quantity in the database."""
        # Insert the unit
        g_id = self.repository.create_global_unit(
            unit_name='gram',
            single_display_name='g',
            plural_display_name='g',
            unit_type='mass',
        )
        # Insert the ingredient
        ingredient_id = self.repository.create_ingredient_name(
            name="Test Ingredient",
        )
        # Insert the nutrient
        nutrient_id = self.repository.create_global_nutrient(
            name="Test Nutrient",
            parent_id=3,
        )
        # Check there are no nutrient quantities in the ingredient
        nutrients = self.repository.read_ingredient_nutrient_quantities(ingredient_id)
        # Add the nutrient to the ingredient
        self.repository.create_ingredient_nutrient_quantity(
            ingredient_id=ingredient_id,
            nutrient_id=nutrient_id,
            ntr_mass_value=1,
            ntr_mass_unit_id=g_id,
            ing_qty_value=100,
            ing_qty_unit_id=g_id,
        )
        # Fetch the ingredient nutrients again
        nutrients = self.repository.read_ingredient_nutrient_quantities(ingredient_id)
        # Check the nutrient is on the ingredient
        self.assertIn(nutrient_id, nutrients.keys())
        # Check the nutrient mass value is correct
        self.assertEqual(nutrients[nutrient_id]["ntr_mass_value"], 1)
        # Check the ingredient quantity value is correct
        self.assertEqual(nutrients[nutrient_id]["ing_qty_value"], 100)
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
        recipe_id = self.repository.create_recipe_name(
            name=recipe_name,
        )
        # Check the name is in the database
        all_recipes = self.repository.read_all_recipe_names()
        self.assertIn(recipe_id, all_recipes.keys())
        # Check the name is correct
        self.assertEqual(all_recipes[recipe_id], recipe_name)
        # Update the recipe name
        self.repository.update_recipe_name(
            recipe_id=recipe_id,
            name=new_recipe_name,
        )
        # Fetch all the recipes again
        all_recipes = self.repository.read_all_recipe_names()
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
        recipe_id = self.repository.create_recipe_name(
            name=recipe_name,
        )
        # Check the description is none
        description = self.repository.read_recipe_description(recipe_id)
        self.assertIsNone(description)
        # Update the recipe description
        self.repository.update_recipe_description(
            recipe_id=recipe_id,
            description=description_1,
        )
        # Fetch the recipe description again
        description = self.repository.read_recipe_description(recipe_id)
        # Check the new recipe description is in the database
        self.assertEqual(description, description_1)
        # Update the recipe description again
        self.repository.update_recipe_description(
            recipe_id=recipe_id,
            description=description_2,
        )
        # Fetch the recipe description again
        description = self.repository.read_recipe_description(recipe_id)
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
        recipe_id = self.repository.create_recipe_name(
            name=recipe_name,
        )
        # Check the instructions are none
        instructions = self.repository.read_recipe_instructions(recipe_id)
        self.assertIsNone(instructions)
        # Update the recipe instructions
        self.repository.update_recipe_instructions(
            recipe_id=recipe_id,
            instructions=instructions_1,
        )
        # Fetch the recipe instructions again
        instructions = self.repository.read_recipe_instructions(recipe_id)
        # Check the new recipe instructions are in the database
        self.assertEqual(instructions, instructions_1)
        # Update the recipe instructions again
        self.repository.update_recipe_instructions(
            recipe_id=recipe_id,
            instructions=instructions_2,
        )
        # Fetch the recipe instructions again
        instructions = self.repository.read_recipe_instructions(recipe_id)
        # Check the new recipe instructions are in the database
        self.assertEqual(instructions, instructions_2)

class TestUpdateRecipeIngredient(DatabaseTestCase):
    """Test the update_recipe_ingredient method of the Repository class."""

    def test_update_recipe_ingredient_updates_ingredient(self):
        """Test that the method updates a recipe ingredient in the database."""
        # Insert the unit
        g_id = self.repository.create_global_unit(
            unit_name='gram',
            single_display_name='g',
            plural_display_name='g',
            unit_type='mass',
        )
        # Insert the recipe
        recipe_id = self.repository.create_recipe_name(
            name="Test Recipe",
        )
        # Insert the ingredient
        ingredient_id = self.repository.create_ingredient_name(
            name="Test Ingredient",
        )
        # Check the ingredient is not in the recipe
        ingredients = self.repository.read_recipe_ingredient_quantities(recipe_id)
        self.assertNotIn(ingredient_id, ingredients.keys())
        # Add the ingredient to the recipe
        self.repository.create_recipe_ingredient_quantity(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            qty_unit_id=g_id,
            qty_value=100,
            qty_utol=10,
            qty_ltol=15,
        )
        # Fetch the recipe ingredients again
        ingredients = self.repository.read_recipe_ingredient_quantities(recipe_id)
        # Check the ingredient is in the recipe
        self.assertIn(ingredient_id, ingredients.keys())
        # Check the ingredient quantity value is correct
        self.assertEqual(ingredients[ingredient_id]["qty_value"], 100)
        # Check the ingredient quantity unit is correct
        self.assertEqual(ingredients[ingredient_id]["qty_unit_id"], g_id)
        # Check the ingredient quantity upper tolerance is correct
        self.assertEqual(ingredients[ingredient_id]["qty_utol"], 10)
        # Check the ingredient quantity lower tolerance is correct
        self.assertEqual(ingredients[ingredient_id]["qty_ltol"], 15)
        # Update the recipe ingredient
        self.repository.update_recipe_ingredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            qty_unit_id=g_id,
            qty_value=200,
            qty_utol=20,
            qty_ltol=25,
        )
        # Fetch the recipe ingredients again
        ingredients = self.repository.read_recipe_ingredient_quantities(recipe_id)
        # Check the ingredient is in the recipe
        self.assertIn(ingredient_id, ingredients.keys())
        # Check the ingredient quantity value is correct
        self.assertEqual(ingredients[ingredient_id]["qty_value"], 200)
        # Check the ingredient quantity unit is correct
        self.assertEqual(ingredients[ingredient_id]["qty_unit_id"], g_id)
        # Check the ingredient quantity upper tolerance is correct
        self.assertEqual(ingredients[ingredient_id]["qty_utol"], 20)
        # Check the ingredient quantity lower tolerance is correct
        self.assertEqual(ingredients[ingredient_id]["qty_ltol"], 25)

class TestUpdateRecipeServeTimeWindow(DatabaseTestCase):
    """Test the update_recipe_serve_time_window method of the Repository class."""

    def test_update_recipe_serve_time_updates_serve_time_window(self):
        """Test that the method updates a recipe serve time in the database."""
        recipe_name = 'test_recipe'
        serve_time_window_1 = "06:00 - 10:00"
        serve_time_window_2 = "12:00 - 16:00"
        # Insert the recipe
        recipe_id = self.repository.create_recipe_name(
            name=recipe_name,
        )
        # Insert the serve time
        serve_time_id = self.repository.create_recipe_serve_time_window(
            recipe_id=recipe_id,
            serve_time_window=serve_time_window_1,
        )
        # Fetch the recipe serve time again
        serve_time_windows = self.repository.read_recipe_serve_time_windows(
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
        serve_time_windows = self.repository.read_recipe_serve_time_windows(
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
        recipe_id = self.repository.create_recipe_name(
            name=recipe_name,
        )
        # Insert the global tags
        tag_id_1 = self.repository.create_global_recipe_tag(tag_1)
        tag_id_2 = self.repository.create_global_recipe_tag(tag_2)
        tag_id_3 = self.repository.create_global_recipe_tag(tag_3)
        # Attach tags 1 and 2 to the recipe
        self.repository.update_recipe_tags(
            recipe_id=recipe_id,
            recipe_tag_ids=[tag_id_1, tag_id_2],
        )
        # Check the tags went into the recipe
        recipe_tags = self.repository.read_recipe_tags(recipe_id)
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
        recipe_tags = self.repository.read_recipe_tags(recipe_id)
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
        ingredient_id = self.repository.create_ingredient_name(
            name=ingredient_name,
        )
        # Check the ingredient is in the database
        all_ingredients = self.repository.read_all_ingredient_names()
        self.assertIn(ingredient_id, all_ingredients.keys())
        # Delete the ingredient
        self.repository.delete_ingredient(ingredient_id)
        # Fetch all the ingredients again
        all_ingredients = self.repository.read_all_ingredient_names()
        # Check the ingredient is not in the database
        self.assertNotIn(ingredient_id, all_ingredients.keys())

class TestDeleteRecipe(DatabaseTestCase):
    """Test the delete_recipe method of the Repository class."""

    def test_delete_recipe_deletes_recipe(self):
        """Test that the method deletes a recipe in the database."""
        recipe_name = 'test_recipe'
        # Insert the recipe
        recipe_id = self.repository.create_recipe_name(
            name=recipe_name,
        )
        # Check the recipe is in the database
        all_recipes = self.repository.read_all_recipe_names()
        self.assertIn(recipe_id, all_recipes.keys())
        # Delete the recipe
        self.repository.delete_recipe(recipe_id)
        # Fetch all the recipes again
        all_recipes = self.repository.read_all_recipe_names()
        # Check the recipe is not in the database
        self.assertNotIn(recipe_id, all_recipes.keys())
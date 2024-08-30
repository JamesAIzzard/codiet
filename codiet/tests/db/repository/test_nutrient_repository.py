from codiet.tests.db import DatabaseTestCase

class TestNutrientRepository(DatabaseTestCase):

    def setUp(self) -> None:
        super().setUp()

        # Because of the foreign key requirements, we need to create a
        # unit and an ingredient before we can create a nutrient quantity

        # Create a couple of test units
        self.unit_1_id = self.repository.units.create_unit_base(
            unit_name="unit 1",
            single_display_name="unit 1 single",
            plural_display_name="unit 1 plural",
            unit_type="mass"
        )
        self.unit_2_id = self.repository.units.create_unit_base(
            unit_name="unit 2",
            single_display_name="unit 2 single",
            plural_display_name="unit 2 plural",
            unit_type="volume"
        )

        # Create a test parent nutrient
        self.parent_nutrient_1_id = self.repository.nutrients.create_global_nutrient(
            nutrient_name="parent nutrient 1",
            parent_id=None
        )
        # Add a couple of aliases
        self.parent_nutrient_1_alias_1_id = self.repository.nutrients.create_global_nutrient_alias(
            alias="parent nutrient 1 alias 1",
            primary_nutrient_id=self.parent_nutrient_1_id
        )
        self.parent_nutrient_1_alias_2_id = self.repository.nutrients.create_global_nutrient_alias(
            alias="parent nutrient 1 alias 2",
            primary_nutrient_id=self.parent_nutrient_1_id
        )

        # Create a couple of test child nutrients
        self.child_nutrient_1_id = self.repository.nutrients.create_global_nutrient(
            nutrient_name="child nutrient 1",
            parent_id=self.parent_nutrient_1_id
        )
        self.child_nutrient_2_id = self.repository.nutrients.create_global_nutrient(
            nutrient_name="child nutrient 2",
            parent_id=self.parent_nutrient_1_id
        )

        # Create a test ingredient
        self.ingredient_1_id = self.repository.ingredients.create_ingredient(
            ingredient_name="ingredient 1"
        )

        # Create a test ingredient nutrient quantity
        self.ingredient_nutrient_quantity_1_id = self.repository.nutrients.create_ingredient_nutrient_quantity(
            ingredient_id=self.ingredient_1_id,
            nutrient_id=self.parent_nutrient_1_id,
            nutrient_mass_unit_id=self.unit_1_id,
            nutrient_mass_value=1.0,
            ingredient_grams_qty=100.0
        )   

    def test_create_and_read_global_nutrient(self):
        """Check that we can create a parent and child global nutrient."""
        # Parent and child nutrients are created in the setUp method

        # Check both are present and correct if we read global nutrients
        nutrients = self.repository.nutrients.read_global_nutrients()
        # Check the right number come back
        self.assertEqual(len(nutrients), 3)
        # Check the parent nutrient is correct
        for nutrient in nutrients:
            if nutrient["id"] == self.parent_nutrient_1_id:
                self.assertEqual(nutrient["nutrient_name"], "parent nutrient 1")
                self.assertIsNone(nutrient["parent_id"])
                break
        else:
            self.fail("Parent nutrient not found")
        
        # Check the child nutrient is correct
        for nutrient in nutrients:
            if nutrient["id"] == self.child_nutrient_1_id:
                self.assertEqual(nutrient["nutrient_name"], "child nutrient 1")
                self.assertEqual(nutrient["parent_id"], self.parent_nutrient_1_id)
                break
        else:
            self.fail("Child nutrient not found")

    def test_create_and_read_global_nutrient_alias(self):
        """Check that we can create and read a global nutrient alias."""

        # Two aliases are added to parent nutrient 1 in setup

        # Read the aliases for the nutrient
        aliases = self.repository.nutrients.read_global_nutrient_aliases(self.parent_nutrient_1_id)

        # Check the right aliases come back
        self.assertEqual(len(aliases), 2)
        # Check the first alias is present
        for alias in aliases:
            if alias["alias_id"] == self.parent_nutrient_1_alias_1_id:
                self.assertEqual(alias["alias"], "parent nutrient 1 alias 1")
                break
        else:
            self.fail("First alias not found")
        # Check the second alias is present
        for alias in aliases:
            if alias["alias_id"] == self.parent_nutrient_1_alias_2_id:
                self.assertEqual(alias["alias"], "parent nutrient 1 alias 2")
                break
        else:
            self.fail("Second alias not found")

    def test_create_and_read_ingredient_nutrient_quantity(self):
        """Check that we can create and read an ingredient nutrient quantity."""

        # Ingredient nutrient quantity is created in the setUp method

        # Read the quantity back
        quantities = self.repository.nutrients.read_ingredient_nutrient_quantities(
            ingredient_id=self.ingredient_1_id
        )

        # Check the right number come back
        self.assertEqual(len(quantities), 1)
        # Check the quantity data
        self.assertEqual(quantities[0]["id"], self.ingredient_nutrient_quantity_1_id)
        self.assertEqual(quantities[0]["nutrient_id"], self.parent_nutrient_1_id)
        self.assertEqual(quantities[0]["nutrient_mass_unit_id"], self.unit_1_id)
        self.assertEqual(quantities[0]["nutrient_mass_value"], 1.0)
        self.assertEqual(quantities[0]["ingredient_grams_qty"], 100.0)

    def test_update_ingredient_nutrient_quantity(self):
        """Check that we can update an ingredient nutrient quantity."""
        # An ingredient nutrient quantity is created in the setUp method

        # Stash the old data
        old_data = self.repository.nutrients.read_ingredient_nutrient_quantities(
            ingredient_id=self.ingredient_1_id
        )[0]

        # Update the old data
        self.repository.nutrients.update_ingredient_nutrient_quantity(
            ingredient_id=self.ingredient_1_id,
            nutrient_id=self.parent_nutrient_1_id,
            nutrient_mass_unit_id=self.unit_2_id,
            nutrient_mass_value=2.0,
            ingredient_grams_qty=200.0
        )

        # Read the new data
        new_data = self.repository.nutrients.read_ingredient_nutrient_quantities(
            ingredient_id=self.ingredient_1_id
        )[0]

        # Check the data has changed
        self.assertEqual(new_data["nutrient_mass_unit_id"], self.unit_2_id)
        self.assertEqual(new_data["nutrient_mass_value"], 2.0)
        self.assertEqual(new_data["ingredient_grams_qty"], 200.0)

    def test_cant_update_nonexistent_ingredient_nutrient_quantity(self):
        """Check that we can't update a non-existent ingredient nutrient quantity."""
        # Try to update a non-existent quantity
        with self.assertRaises(ValueError):
            self.repository.nutrients.update_ingredient_nutrient_quantity(
                ingredient_id=self.ingredient_1_id,
                nutrient_id=self.child_nutrient_2_id,
                nutrient_mass_unit_id=self.unit_2_id,
                nutrient_mass_value=2.0,
                ingredient_grams_qty=200.0
            )

    def test_delete_ingredient_nutrient_quantity(self):
        """Check that we can delete an ingredient nutrient quantity."""
        # An ingredient nutrient quantity is created in the setUp method

        # Check the quantity is present
        quantities = self.repository.nutrients.read_ingredient_nutrient_quantities(
            ingredient_id=self.ingredient_1_id
        )
        self.assertEqual(len(quantities), 1)

        # Delete the quantity
        self.repository.nutrients.delete_ingredient_nutrient_quantity(
            ingredient_id=self.ingredient_1_id,
            nutrient_id=self.parent_nutrient_1_id
        )

        # Check the quantity is gone
        quantities = self.repository.nutrients.read_ingredient_nutrient_quantities(
            ingredient_id=self.ingredient_1_id
        )
        self.assertEqual(len(quantities), 0)

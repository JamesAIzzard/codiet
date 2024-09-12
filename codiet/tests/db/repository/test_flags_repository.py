from codiet.tests.db.database_test_case import DatabaseTestCase

class TestFlagRepository(DatabaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Create a global flag
        self.flag_1_id = self.repository.flags.create_flag("Test Flag 1")

        # Create an ingredient
        self.ingredient_id = self.repository.ingredients.create_ingredient_base("Test Ingredient")

    def test_create_read_flag(self):
        """Check that we can create and read global flags."""
        # Create a flag
        flag_3_id = self.repository.flags.create_flag("Test Flag 3")

        # Check we got an integer ID
        self.assertIsInstance(flag_3_id, int)

        # Read the flag names and check the new flag is there
        flag_names = self.repository.flags.read_all_global_flag_names()
        self.assertIn("Test Flag 3", flag_names.values())
        self.assertEqual(len(flag_names), 2) # One was created during setup 

    def test_create_read_ingredient_flag(self):
        """Check that we can create and read ingredient flags."""

        # Create an ingredient flag
        ingredient_flag_id = self.repository.flags.create_ingredient_flag(self.ingredient_id, self.flag_1_id, True)

        # Check we got an integer ID
        self.assertIsInstance(ingredient_flag_id, int)

        # Read the flags for the ingredient and check the new flag is there
        ingredient_flags = self.repository.flags.read_ingredient_flags(self.ingredient_id)
        self.assertIn(self.flag_1_id, ingredient_flags)
        self.assertEqual(len(ingredient_flags), 1)

    def test_update_ingredient_flag(self):
        """Check that we can update ingredient flags."""

        # Create an ingredient flag
        _ = self.repository.flags.create_ingredient_flag(self.ingredient_id, self.flag_1_id, True)

        # Check the flag value is True
        ingredient_flags = self.repository.flags.read_ingredient_flags(self.ingredient_id)
        self.assertIn(self.flag_1_id, ingredient_flags)
        self.assertEqual(len(ingredient_flags), 1)

        # Update the flag value
        self.repository.flags.update_ingredient_flag(self.ingredient_id, self.flag_1_id, False)

        # Check the flag value is False
        all_flags = self.repository.flags.read_ingredient_flags(self.ingredient_id)
        self.assertIn(self.flag_1_id, all_flags)
        self.assertEqual(len(all_flags), 1)
        for ing_flag_data in all_flags.values():
            if ing_flag_data["flag_id"] == self.flag_1_id:
                self.assertEqual(ing_flag_data["flag_value"], False)

    def test_exception_if_update_flag_not_exist(self):
        """Check that we get an exception if we try to update a flag that doesn't exist."""
        # Check we get an exception if we try to update a flag that doesn't exist
        with self.assertRaises(ValueError):
            self.repository.flags.update_ingredient_flag(self.ingredient_id, 1, True)

    def test_delete_ingredient_flag(self):
        """Check that we can delete ingredient flags."""
        # Create an ingredient flag
        _ = self.repository.flags.create_ingredient_flag(self.ingredient_id, self.flag_1_id, True)

        # Check the flag is there
        ingredient_flags = self.repository.flags.read_ingredient_flags(self.ingredient_id)
        self.assertIn(self.flag_1_id, ingredient_flags)
        self.assertEqual(len(ingredient_flags), 1)

        # Delete the flag
        self.repository.flags.delete_ingredient_flag(self.ingredient_id, self.flag_1_id)

        # Check the flag is gone
        ingredient_flags = self.repository.flags.read_ingredient_flags(self.ingredient_id)
        self.assertEqual(len(ingredient_flags), 0)
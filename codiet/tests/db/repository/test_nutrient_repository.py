from codiet.tests.db import DatabaseTestCase

class TestNutrientRepository(DatabaseTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_create_and_read_global_nutrient(self):
        """Check that we can create a parent and child global nutrient."""
        # Create the parent nutrient
        parent_id = self.repository.nutrients.create_global_nutrient(
            nutrient_name="Parent Nutrient",
            parent_id=None
        )

        # Create the child nutrient
        child_id = self.repository.nutrients.create_global_nutrient(
            nutrient_name="Child Nutrient",
            parent_id=parent_id
        )

        # Check both are present and correct if we read global nutrients
        nutrients = self.repository.nutrients.read_global_nutrients()
        # Check the right number come back
        self.assertEqual(len(nutrients), 2)
        # Check the parent nutrient is correct
        for nutrient in nutrients:
            if nutrient["id"] == parent_id:
                self.assertEqual(nutrient["nutrient_name"], "Parent Nutrient")
                self.assertIsNone(nutrient["parent_id"])
                break
        else:
            self.fail("Parent nutrient not found")
        
        # Check the child nutrient is correct
        for nutrient in nutrients:
            if nutrient["id"] == child_id:
                self.assertEqual(nutrient["nutrient_name"], "Child Nutrient")
                self.assertEqual(nutrient["parent_id"], parent_id)
                break
        else:
            self.fail("Child nutrient not found")

    def test_create_and_read_global_nutrient_alias(self):
        """Check that we can create and read a global nutrient alias."""
        # Create the nutrient
        nutrient_id = self.repository.nutrients.create_global_nutrient(
            nutrient_name="Nutrient",
            parent_id=None
        )

        # Create a couple of aliases
        alias1_id = self.repository.nutrients.create_global_nutrient_alias(
            alias="Alias 1",
            primary_nutrient_id=nutrient_id
        )
        alias2_id = self.repository.nutrients.create_global_nutrient_alias(
            alias="Alias 2",
            primary_nutrient_id=nutrient_id
        )

        # Read the aliases for the nutrient
        aliases = self.repository.nutrients.read_global_nutrient_aliases(nutrient_id)

        # Check the right number come back
        self.assertEqual(len(aliases), 2)
        # Check the first alias data
        for alias in aliases:
            if alias["alias_id"] == alias1_id:
                self.assertEqual(alias["alias"], "Alias 1")
                break
        else:
            self.fail("Alias 1 not found")
        # Check the second alias data
        for alias in aliases:
            if alias["alias_id"] == alias2_id:
                self.assertEqual(alias["alias"], "Alias 2")
                break
        else:
            self.fail("Alias 2 not found")
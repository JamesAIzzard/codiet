from codiet.tests.db.database_test_case import DatabaseTestCase
from codiet.models.nutrients.nutrient import Nutrient

class TestNutrientDBService(DatabaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        
        # Create some test global nutrient instances
        self.parent_nutrient = Nutrient(
            nutrient_name="Test Nutrient 1",
            aliases={"Test Nutrient 1 Alias 1", "Test Nutrient 1 Alias 2"},
            parent=None
        )
        self.child_nutrient_1 = Nutrient(
            nutrient_name="Test Nutrient 2",
            aliases={"Test Nutrient 2 Alias 1", "Test Nutrient 2 Alias 2"},
            parent=self.parent_nutrient
        )
        self.child_nutrient_2 = Nutrient(
            nutrient_name="Test Nutrient 3",
            aliases={"Test Nutrient 3 Alias 1", "Test Nutrient 3 Alias 2"},
            parent=self.parent_nutrient
        )

        # Save them to the database
        self.db_service.nutrients.create_global_nutrients({
            self.parent_nutrient,
            self.child_nutrient_1,
            self.child_nutrient_2
        })

    def test_global_nutrient_id_name_map(self) -> None:
        """Checks that the global nutrient id-name map contains the correct
        mappings for the correct nutrients."""
        # Test nutrients saved to the database during setup
        # Get the global nutrient id-name map
        nutrient_id_name_map = self.db_service.nutrients.global_nutrient_id_name_map

        # Check that the map contains the correct mappings
        self.assertEqual(
            nutrient_id_name_map.get_value(self.parent_nutrient.id), # type: ignore
            self.parent_nutrient.nutrient_name
        )
        self.assertEqual(
            nutrient_id_name_map.get_value(self.child_nutrient_1.id), # type: ignore
            self.child_nutrient_1.nutrient_name
        )
        self.assertEqual(
            nutrient_id_name_map.get_value(self.child_nutrient_2.id), # type: ignore
            self.child_nutrient_2.nutrient_name
        )


    def test_global_nutrients(self) -> None:
        # Check that we get a collection of the right number of nutrient instances
        nutrients = self.db_service.nutrients.global_nutrients

        self.assertEqual(len(nutrients), 3)
        self.assertIn(self.parent_nutrient, nutrients)
        self.assertIn(self.child_nutrient_1, nutrients)
        self.assertIn(self.child_nutrient_2, nutrients)

    def test_get_nutrient_by_name(self) -> None:
        # Check that we can fetch a nutrient instance by its name
        nutrient = self.db_service.nutrients.get_nutrient_by_name("Test Nutrient 1")

        self.assertEqual(nutrient, self.parent_nutrient)

    def test_get_nutrient_by_id(self) -> None:
        # Check that we can fetch a nutrient instance by its ID
        nutrient = self.db_service.nutrients.get_nutrient_by_id(self.parent_nutrient.id) # type: ignore (parent_nutrient is not None)

        self.assertEqual(nutrient, self.parent_nutrient)

    def test_create_global_nutrient(self) -> None:
        """Confirms that we can create a new global nutrient."""
        # Create a nutrient instance
        nutrient = Nutrient(
            nutrient_name="Test Nutrient 4",
            aliases={"Test Nutrient 4 Alias 1", "Test Nutrient 4 Alias 2"},
            parent=None
        )

        # Assert that it is not yet in the database by reading all existing nutrients
        nutrients = self.db_service.nutrients.global_nutrients
        self.assertNotIn(nutrient, nutrients)

        # Save the nutrient to the database
        self.db_service.nutrients.create_global_nutrient(nutrient)

        # Assert that the nutrient is now in the database
        nutrients = self.db_service.nutrients.global_nutrients
        self.assertIn(nutrient, nutrients)


    def test_create_global_nutrients(self) -> None:
        """Confirms that we can create multiple new global nutrients."""
        # Create two additional global nutrients
        nutrient_1 = Nutrient(
            nutrient_name="Test Nutrient 4",
            aliases={"Test Nutrient 4 Alias 1", "Test Nutrient 4 Alias 2"},
            parent=None
        )
        nutrient_2 = Nutrient(
            nutrient_name="Test Nutrient 5",
            aliases={"Test Nutrient 5 Alias 1", "Test Nutrient 5 Alias 2"},
            parent=None
        )

        # Assert that neither of these are in the database, by reading existing nutrients
        nutrients = self.db_service.nutrients.global_nutrients
        self.assertNotIn(nutrient_1, nutrients)
        self.assertNotIn(nutrient_2, nutrients)

        # Save the nutrients to the database
        self.db_service.nutrients.create_global_nutrients({nutrient_1, nutrient_2})

        # Assert that the nutrients are now in the database
        nutrients = self.db_service.nutrients.global_nutrients
        self.assertIn(nutrient_1, nutrients)
        self.assertIn(nutrient_2, nutrients)


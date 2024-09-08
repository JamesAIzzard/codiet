from codiet.tests.db.database_test_case import DatabaseTestCase
from codiet.models.nutrients.nutrient import Nutrient

class TestNutrientDBService(DatabaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        
        # Create some test nutrient instances
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
        pass

    def test_get_nutrient_by_name(self) -> None:
        pass

    def test_get_nutrient_by_id(self) -> None:
        pass

    def test_create_global_nutrient(self) -> None:
        pass

    def test_create_global_nutrients(self) -> None:
        pass


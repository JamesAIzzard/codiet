from unittest.mock import Mock

from codiet.tests.db.database_test_case import DatabaseTestCase
from codiet.tests.fixtures.units_test_fixtures import UnitsTestFixtures
from codiet.tests.fixtures.nutrient_test_fixtures import NutrientTestFixtures
from codiet.models.nutrients.nutrient import Nutrient
from codiet.models.ingredients.ingredient import Ingredient
from codiet.models.nutrients.ingredient_nutrient_quantity import IngredientNutrientQuantity

class TestNutrientDBService(DatabaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        
        self.units_fixtures = UnitsTestFixtures(self.db_service)
        self.nutrients_fixtures = NutrientTestFixtures(self.db_service)

    def test_global_nutrient_id_name_map(self) -> None:
        """Checks that the global nutrient id-name map contains the correct
        mappings for the correct nutrients."""
        self.nutrients_fixtures.setup_test_nutrients()

        # Get the global nutrient id-name map
        nutrient_id_name_map = self.db_service.nutrients.global_nutrient_id_name_map

        # Check a couple of the mappings are correct
        self.assertEqual(
            nutrient_id_name_map.get_value(self.nutrients_fixtures.test_nutrients["protein"].id), # type: ignore
            "protein"
        )
        self.assertEqual(
            nutrient_id_name_map.get_value(self.nutrients_fixtures.test_nutrients["carbohydrate"].id), # type: ignore
            "carbohydrate"
        )

    def test_global_nutrients(self) -> None:
        """Checks that the global nutrients property returns the correct nutrients."""
        self.nutrients_fixtures.setup_test_nutrients()

        # Check that we get a collection of the right number of nutrient instances
        nutrients = self.db_service.nutrients.global_nutrients

        # Check that the nutrients retured are those in the fixture
        self.assertCountEqual(nutrients, self.nutrients_fixtures.test_nutrients.values())

    def test_get_nutrient_by_name(self) -> None:
        """Checks that we can fetch a nutrient instance by its name."""
        self.nutrients_fixtures.setup_test_nutrients()

        # Check that we can fetch a nutrient instance by its name
        nutrient = self.db_service.nutrients.get_nutrient_by_name("protein")

        self.assertEqual(nutrient, self.nutrients_fixtures.test_nutrients["protein"])

    def test_get_nutrient_by_id(self) -> None:
        """Checks that we can fetch a nutrient instance by its id."""
        self.nutrients_fixtures.setup_test_nutrients()

        # Check that we can fetch a nutrient instance by its id
        nutrient = self.db_service.nutrients.get_nutrient_by_id(self.nutrients_fixtures.test_nutrients["protein"].id) # type: ignore

        self.assertEqual(nutrient, self.nutrients_fixtures.test_nutrients["protein"])

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

    def test_create_ingredient_nutrient_quantity(self) -> None:
        """Checks that we can create an ingredient nutrient quantity."""
        # Created in setup, check that it was created



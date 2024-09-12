"""Test fixtures for tests requiring nutrient instances."""

from codiet.db.database_service import DatabaseService
from codiet.models.nutrients.nutrient import Nutrient

class NutrientTestFixtures:
    """Test fixtures class for nutrients."""

    def __init__(self, db_service:DatabaseService) -> None:
        self._db_service = db_service
        self._test_nutrients:dict[str, Nutrient]|None = None
        self._test_nutrients_setup:bool = False

    @property
    def test_nutrients(self) -> dict[str, Nutrient]:
        """Returns the test nutrients."""
        if self._test_nutrients is None:
            self._test_nutrients = self._create_test_nutrients()
        return self._test_nutrients

    def setup_test_nutrients(self) -> None:
        """Sets up the test nutrients in the database."""
        self._db_service.nutrients.create_global_nutrients(self.test_nutrients.values())
        self._test_nutrients_setup = True

    def _create_test_nutrients(self) -> dict[str, Nutrient]:
        """Instantiates a dictionary of nutrients for testing purposes."""
        # Instantiate some test nutrients
        protein = Nutrient(
            nutrient_name="protein"
        )

        carbohydrate = Nutrient(
            nutrient_name="carbohydrate",
            aliases=["carb", "carbs"]
        )

        glucose = Nutrient(
            nutrient_name="glucose"
        )

        valine = Nutrient(
            nutrient_name="valine"
        )

        # Configure parent child relationships
        protein._set_children([valine])
        valine._set_parent(protein)
        carbohydrate._set_children([glucose])
        glucose._set_parent(carbohydrate)

        # Build and return the dict
        return {
            "protein": protein,
            "carbohydrate": carbohydrate,
            "glucose": glucose,
            "valine": valine
        }

from typing import TYPE_CHECKING

from codiet.tests.fixtures import BaseTestFixtures
from codiet.model.nutrients import Nutrient, NutrientQuantity

if TYPE_CHECKING:
    from codiet.db import DatabaseService
    from codiet.model.ingredients import Ingredient

class NutrientTestFixtures(BaseTestFixtures):

    def __init__(self) -> None:

        self._nutrients:dict[str, Nutrient]|None = None

    @property
    def nutrients(self) -> dict[str, Nutrient]:
        """Returns the test nutrients."""
        if self._nutrients is None:
            self._nutrients = self._create_test_nutrients()
        return self._nutrients

    def get_nutrient_by_name(self, nutrient_name:str) -> Nutrient:
        """Returns a nutrient by name."""
        return self.nutrients[nutrient_name]

    def create_nutrient_quantity(self, nutrient_name:str) -> NutrientQuantity:
        nutrient = self.get_nutrient_by_name(nutrient_name)
        return NutrientQuantity(nutrient)

    def setup_database_nutrients(self, db_service:'DatabaseService') -> None:
        """Sets up the test nutrients in the database."""
        db_service.nutrients.create_global_nutrients(self.nutrients.values())

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
        fat = Nutrient(
            nutrient_name="fat"
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
            "valine": valine,
            "fat": fat
        }

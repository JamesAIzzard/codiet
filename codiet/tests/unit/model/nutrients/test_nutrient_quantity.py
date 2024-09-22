"""Tests for the NutrientQuantity class."""

from codiet.tests import BaseCodietTest
from codiet.model.nutrients import NutrientQuantity

class BaseNutrientQuantityTest(BaseCodietTest):
    """Base class for testing NutrientQuantity elements."""

    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseNutrientQuantityTest):
    """Tests for the NutrientQuantity constructor."""

    def test_minimal_arguments(self) -> None:
        """Test the constructor with the minimum required parameters."""
        protein = self.nutrient_fixtures.get_nutrient_by_name("protein")
        protein_quantity = NutrientQuantity(protein)
        self.assertIsInstance(protein_quantity, NutrientQuantity)

    def test_nutrient_is_assigned(self) -> None:
        """Test that the nutrient is assigned correctly."""
        protein = self.nutrient_fixtures.get_nutrient_by_name("protein")
        protein_quantity = NutrientQuantity(protein)
        self.assertIs(protein, protein_quantity.nutrient)

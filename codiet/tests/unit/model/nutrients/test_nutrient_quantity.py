from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.nutrients import NutrientTestFixtures
from codiet.model.nutrients import NutrientQuantity

class BaseNutrientQuantityTest(BaseCodietTest):

    def setUp(self) -> None:
        super().setUp()
        self.nutrient_fixtures = NutrientTestFixtures.get_instance()

class TestConstructor(BaseNutrientQuantityTest):

    def test_minimal_arguments(self) -> None:
        protein = self.nutrient_fixtures.get_nutrient_by_name("protein")
        protein_quantity = NutrientQuantity(protein)
        self.assertIsInstance(protein_quantity, NutrientQuantity)

    def test_nutrient_is_assigned(self) -> None:
        protein = self.nutrient_fixtures.get_nutrient_by_name("protein")
        protein_quantity = NutrientQuantity(protein)
        self.assertIs(protein, protein_quantity.nutrient)

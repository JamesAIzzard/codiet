from codiet.tests import BaseCodietTest
from codiet.data import DatabaseService
from codiet.model.nutrients import NutrientQuantity

class BaseNutrientQuantityTest(BaseCodietTest):
    pass

class TestConstructor(BaseNutrientQuantityTest):

    def test_can_create_instance(self) -> None:
        protein = DatabaseService().read_nutrient("protein")
        protein_quantity = NutrientQuantity(protein)
        self.assertIsInstance(protein_quantity, NutrientQuantity)

    def test_nutrient_is_singleton(self) -> None:
        protein = DatabaseService().read_nutrient("protein")
        protein_quantity = NutrientQuantity(protein)
        self.assertIs(protein_quantity.nutrient, DatabaseService().read_nutrient("protein"))

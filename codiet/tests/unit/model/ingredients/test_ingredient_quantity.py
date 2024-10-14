from codiet.tests import BaseCodietTest

from codiet.model.nutrients import NutrientQuantity

class BaseTestIngredientQuantity(BaseCodietTest):
    pass

class TestNutrientQuantities(BaseTestIngredientQuantity):
    def test_returns_correct_nutrient_quantities(self):
        oats_100g = self.ingredient_factory.create_ingredient_quantity(
            ingredient_name="oats",
            quantity_unit_name="gram",
            quantity_value=100
        )

        for nutrient_quantity in oats_100g.nutrient_quantities.values():
            self.assertIsInstance(nutrient_quantity, NutrientQuantity)

        protein_quantity = oats_100g.nutrient_quantities["protein"].quantity
        carbohydrate_quantity = oats_100g.nutrient_quantities["carbohydrate"].quantity
        fat_quantity = oats_100g.nutrient_quantities["fat"].quantity

        protein_grams = self.unit_conversion_service.convert_to_grams(protein_quantity).value
        carbohydrate_grams = self.unit_conversion_service.convert_to_grams(carbohydrate_quantity).value
        fat_grams = self.unit_conversion_service.convert_to_grams(fat_quantity).value

        self.assertAlmostEqual(protein_grams, 17, places=3)
        self.assertAlmostEqual(carbohydrate_grams, 60, places=3)
        self.assertAlmostEqual(fat_grams, 7, places=3)
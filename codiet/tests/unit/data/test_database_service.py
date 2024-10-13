from codiet.tests import BaseCodietTest
from codiet.data import NutrientNotFoundError, IngredientNotFoundError, RecipeNotFoundError

class BaseDatabaseServiceTest(BaseCodietTest):
    pass

class TestReadNutrient(BaseDatabaseServiceTest):
    def test_nutrient_missing_causes_nutrient_not_found_error(self):
        with self.assertRaises(NutrientNotFoundError):
            self.database_service.read_nutrient("missing_nutrient")

class TestReadIngredient(BaseDatabaseServiceTest):
    def test_ingredient_missing_causes_ingredient_not_found_error(self):
        with self.assertRaises(IngredientNotFoundError):
            self.database_service.read_ingredient("missing_ingredient")

class TestReadRecipe(BaseDatabaseServiceTest):
    def test_recipe_missing_causes_recipe_not_found_error(self):
        with self.assertRaises(RecipeNotFoundError):
            self.database_service.read_recipe("missing_recipe")
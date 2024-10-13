from codiet.tests import BaseCodietTest
from codiet.model.nutrients import NutrientQuantity

class BaseTestRecipe(BaseCodietTest):
    pass

class TestFlags(BaseTestRecipe):
    def test_flags_are_correct(self):
        recipe = self.database_service.read_recipe("apple_pie")

        self.assertFalse(recipe.get_flag("vegan").value)
        self.assertTrue(recipe.get_flag("vegetarian").value)
        self.assertFalse(recipe.get_flag("gluten_free").value)

class TestTotalGramsInDefinition(BaseTestRecipe):
    def test_returns_correct_value(self):
        recipe = self.database_service.read_recipe("apple_pie")

        self.assertEqual(recipe.total_grams_in_definition, (4*182)+150+200+200)

class TestAddIngredientQuantity(BaseTestRecipe):
    def test_can_add_ingredient_quantity(self):
        recipe = self.recipe_factory.create_recipe(name="Oatmeal")
        oats = self.ingredient_factory.create_ingredient_quantity(
            ingredient_name="oats",
            quantity_unit_name="gram",
            quantity_value=100
        )

        self.assertNotIn("oats", recipe.ingredient_quantities)

        recipe.add_ingredient_quantity(oats)

        self.assertIn(oats, recipe.ingredient_quantities.values())

    def test_exception_if_ingredient_quantity_already_added(self):
        recipe = self.recipe_factory.create_recipe(name="Oatmeal")
        oats = self.ingredient_factory.create_ingredient_quantity(
            ingredient_name="oats",
            quantity_unit_name="gram",
            quantity_value=100
        )

        recipe.add_ingredient_quantity(oats)

        with self.assertRaises(ValueError):
            recipe.add_ingredient_quantity(oats)

class TestNutrientsDefinedOnAllIngredients(BaseTestRecipe):
    def test_returns_correct_nutrients(self):
        recipe = self.database_service.read_recipe("apple_pie")

        self.assertEqual(len(recipe.nutrients_defined_on_all_ingredients), 3)
        self.assertIn("protein", recipe.nutrients_defined_on_all_ingredients)
        self.assertIn("carbohydrate", recipe.nutrients_defined_on_all_ingredients)
        self.assertIn("fat", recipe.nutrients_defined_on_all_ingredients)

class TestNutrientQuantities(BaseTestRecipe):

    def test_returns_nutrient_quantities(self):
        recipe = self.database_service.read_recipe("apple_pie")

        for nutrient_quantity in recipe.nutrient_quantities.values():
            self.assertIsInstance(nutrient_quantity, NutrientQuantity)

    def test_returns_correct_nutrient_quantities(self):
        trail_mix = self.database_service.read_recipe("trail_mix")

        # Sum protein in trail mix
        trail_mix_protein = (100*0.15)+(100*0.26)+(100*0.15)

        self.assertEqual(trail_mix.nutrient_quantities["protein"].quantity, trail_mix_protein)
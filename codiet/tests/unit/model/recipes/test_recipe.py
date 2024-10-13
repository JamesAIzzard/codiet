from codiet.tests import BaseCodietTest

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
from codiet.tests import BaseCodietTest

class BaseTestRecipe(BaseCodietTest):
    pass

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

        self.assertIn(oats, recipe.ingredient_quantities)

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
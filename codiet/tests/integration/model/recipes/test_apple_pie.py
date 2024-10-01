from unittest import skip

from codiet.tests import BaseCodietTest

from codiet.model.recipes import Recipe

class BaseApplePieTest(BaseCodietTest):

    def setUp(self) -> None:
        super().setUp()
        self.recipe_fixtures = RecipeTestFixtures.get_instance()

class TestCreateRecipe(BaseApplePieTest):

    def test_can_make_apple_pie(self):
        apple_pie = self.recipe_fixtures.apple_pie
        self.assertIsInstance(apple_pie, Recipe)

class TestFlags(BaseApplePieTest):
    @skip("Not implemented")
    def test_apple_pie_is_vegetarian(self):
        apple_pie = self.recipe_fixtures.apple_pie
        
        self.assertTrue(apple_pie.get_flag("vegetarian").value)

    def test_apple_pie_is_not_vegan(self):
        apple_pie = self.recipe_fixtures.apple_pie
        
        self.assertFalse(apple_pie.get_flag("vegan").value)

    def test_apple_pie_is_not_gluten_free(self):
        apple_pie = self.recipe_fixtures.apple_pie
        
        self.assertFalse(apple_pie.get_flag("gluten_free").value)
from codiet.tests import BaseCodietTest

from codiet.model.recipes import Recipe

class TestCreateApplePie(BaseCodietTest):

    def test_can_make_apple_pie(self):
        apple_pie = self.recipe_fixtures.apple_pie
        self.assertIsInstance(apple_pie, Recipe)
from codiet.tests import BaseModelTest

from codiet.model.recipes import Recipe

class TestCreateApplePie(BaseModelTest):

    def test_can_make_apple_pie(self):
        apple_pie = self.recipe_fixtures.apple_pie
        self.assertIsInstance(apple_pie, Recipe)
from codiet.tests import BaseCodietTest
from codiet.tests.fixtures import RecipeTestFixtures

from codiet.model.recipes import Recipe

class BaseApplePieTest(BaseCodietTest):

    def setUp(self) -> None:
        super().setUp()
        self.recipe_fixtures = RecipeTestFixtures.get_instance()

class TestCreateApplePie(BaseApplePieTest):

    def test_can_make_apple_pie(self):
        apple_pie = self.recipe_fixtures.apple_pie
        self.assertIsInstance(apple_pie, Recipe)
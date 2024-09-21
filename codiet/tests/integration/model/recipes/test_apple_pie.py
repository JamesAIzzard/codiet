from codiet.tests import BaseModelTest
from codiet.tests.fixtures.ingredients import IngredientTestFixtures
from codiet.tests.fixtures.time import TimeTestFixtures
from codiet.model.recipes import Recipe

class BaseRecipeIntegrationTest(BaseModelTest):

    def setUp(self) -> None:
        super().setUp()
        self.ingredient_fixtures = IngredientTestFixtures.initialise()
        self.time_fixtures = TimeTestFixtures.initialise()

class TestCreateApplePie(BaseRecipeIntegrationTest):

    def test_can_make_apple_pie(self):
        apple_pie = self.make_apple_pie()
        self.assertIsInstance(apple_pie, Recipe)
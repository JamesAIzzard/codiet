from codiet.tests import BaseCodietTest
from codiet.tests.fixtures import IngredientTestFixtures
from codiet.model.ingredients import Ingredient

class BaseAppleTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()
        self.ingredient_fixtures = IngredientTestFixtures.get_instance()

class TestCreateApple(BaseAppleTest):

    def test_can_create_apple(self):
        apple = self.ingredient_fixtures.get_ingredient_by_name("apple")
        self.assertIsInstance(apple, Ingredient)
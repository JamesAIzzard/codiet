from codiet.tests import BaseCodietTest
from codiet.model.ingredients import Ingredient

class TestCreateApple(BaseCodietTest):

    def test_can_create_apple(self):
        apple = self.ingredient_fixtures.get_ingredient_by_name("apple")
        self.assertIsInstance(apple, Ingredient)
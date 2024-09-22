from codiet.tests import BaseModelTest
from codiet.model.ingredients import Ingredient

class TestCreateApple(BaseModelTest):

    def test_can_create_apple(self):
        apple = self.ingredient_fixtures.get_ingredient_by_name("apple")
        self.assertIsInstance(apple, Ingredient)
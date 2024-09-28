from codiet.tests import BaseCodietTest
from codiet.model.ingredients import IngredientQuantity
from codiet.model.quantities import Quantity

class BaseIngredientQuantityTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()
        self.ingredient_fixtures = self.fixture_manager.ingredient_fixtures

class TestConstructor(BaseIngredientQuantityTest):

    def test_construct_from_ingredient_name(self):
        apple_quantity = IngredientQuantity.from_ingredient_name("apple")
        self.assertIsInstance(apple_quantity, IngredientQuantity)

    def test_construct_from_ingredient(self):
        apple = self.ingredient_fixtures.create_test_ingredient("apple")
        apple_quantity = IngredientQuantity.from_ingredient(apple)
        self.assertIsInstance(apple_quantity, IngredientQuantity)

    def test_ingredient_is_set(self):
        apple = self.ingredient_fixtures.create_test_ingredient("apple")
        apple_quantity = IngredientQuantity.from_ingredient(apple)
        self.assertIs(apple_quantity.ingredient, apple)
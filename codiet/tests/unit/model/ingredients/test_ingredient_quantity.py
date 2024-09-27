from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.ingredients import IngredientTestFixtures
from codiet.model.domain_service import DomainService
from codiet.model.ingredients import IngredientQuantity
from codiet.model.quantities import Quantity

class BaseIngredientQuantityTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()
        self.ingredient_fixtures = IngredientTestFixtures.get_instance()
        self.domain_service = DomainService.get_instance()

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

    def test_quantity_unit_is_set(self):
        apple_quantity = IngredientQuantity(
            self.ingredient_fixtures.create_test_ingredient("apple"),
            quantity=Quantity(self.domain_service.get_unit("kilogram"))
        )
        kilogram = self.domain_service.get_unit("kilogram")
        self.assertIs(apple_quantity.quantity.unit, kilogram)
from codiet.tests import BaseCodietTest
from codiet.model.ingredients import IngredientQuantity
from codiet.model.quantities import Quantity

class TestConstructor(BaseCodietTest):

    def test_minimal_arguments(self):
        apple_quantity = self.ingredient_fixtures.create_ingredient_quantity("apple")
        self.assertIsInstance(apple_quantity, IngredientQuantity)

    def test_ingredient_is_set(self):
        apple = self.ingredient_fixtures.get_ingredient_by_name("apple")
        apple_quantity = IngredientQuantity(apple)
        self.assertIs(apple_quantity.ingredient, apple)

    def test_empty_quantity_unit_gets_default(self):
        apple_quantity = IngredientQuantity(
            self.ingredient_fixtures.get_ingredient_by_name("apple")
        )
        
        self.assertIs(apple_quantity.quantity.unit, self.domain_service.gram)

    def test_quantity_unit_is_set(self):
        apple_quantity = IngredientQuantity(
            self.ingredient_fixtures.get_ingredient_by_name("apple"),
            quantity=Quantity(self.domain_service.get_unit("kilogram"))
        )
        kilogram = self.domain_service.get_unit("kilogram")
        self.assertIs(apple_quantity.quantity.unit, kilogram)
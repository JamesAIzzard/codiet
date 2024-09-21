from codiet.tests import BaseModelTest
from codiet.tests.fixtures.ingredients import IngredientTestFixtures
from codiet.tests.fixtures.quantities import QuantitiesTestFixtures
from codiet.tests.fixtures.ingredients import create_apple
from codiet.model.ingredients import Ingredient

class BaseAppleIntegrationTest(BaseModelTest):

    def setUp(self) -> None:
        super().setUp()
        self.ingredient_fixtures = IngredientTestFixtures()
        self.unit_fixtures = QuantitiesTestFixtures()

class TestCreateApple(BaseAppleIntegrationTest):

    def test_can_create_apple(self):
        apple = create_apple()
        self.assertIsInstance(apple, Ingredient)
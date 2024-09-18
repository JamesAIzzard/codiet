from codiet.tests import BaseModelTest
from codiet.tests.fixtures import IngredientTestFixtures

class BaseRecipeTest(BaseModelTest):
    """Base class for testing Recipe elements."""

    def setUp(self) -> None:
        super().setUp()
        self.ingredient_fixtures = IngredientTestFixtures()
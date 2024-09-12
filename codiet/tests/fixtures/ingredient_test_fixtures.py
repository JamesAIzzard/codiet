"""Test fixtures for tests requiring ingredient instances."""

from codiet.tests.fixtures.units_test_fixtures import UnitsTestFixtures
from codiet.models.ingredients.ingredient import Ingredient

class IngredientTestFixtures:
    """Test fixtures class for ingredients."""

    def __init__(self, units_test_fixtures:UnitsTestFixtures) -> None:
        self._units_test_fixtures = units_test_fixtures
        self._db_service = self._units_test_fixtures._db_service

        # Configure the units and unit conversions
        self._units_test_fixtures.setup_test_global_unit_conversions()

        # Initialise the ingredient class level attributes
        Ingredient.initialise_class(self._db_service.units)

        self._test_ingredients:dict[str, Ingredient]|None = None
        self._test_ingredients_setup:bool = False

    @property
    def test_ingredients(self) -> dict[str, Ingredient]:
        """Returns the test ingredients."""
        if self._test_ingredients is None:
            self._test_ingredients = self._create_test_ingredients()
        return self._test_ingredients
    
    def setup_test_ingredients(self) -> None:
        """Sets up the test ingredients in the database."""
        self._db_service.ingredients.create_ingredients(self.test_ingredients.values())
        self._test_ingredients_setup = True

    def _create_test_ingredients(self) -> dict[str, Ingredient]:
        """Instantiates a dictionary of ingredients for testing purposes."""
        return {
            "apple": Ingredient(
                name="apple",
                description="A fruit",
                cost_value=1.0,
                cost_qty_value=1.0,
                cost_qty_unit=self._db_service.units.get_unit_by_name("kilogram"),
                gi=40.0
            ),
            "banana": Ingredient(
                name="banana",
                description="A fruit",
                cost_value=2.0,
                cost_qty_value=1.0,
                cost_qty_unit=self._db_service.units.get_unit_by_name("kilogram"),
                gi=50.0
            ),
            "chicken": Ingredient(
                name="chicken",
                description="A meat",
                cost_value=3.0,
                cost_qty_value=1.0,
                cost_qty_unit=self._db_service.units.get_unit_by_name("kilogram"),
                gi=60.0
            ),
            "potato": Ingredient(
                name="potato",
                description="A vegetable",
                cost_value=4.0,
                cost_qty_value=1.0,
                cost_qty_unit=self._db_service.units.get_unit_by_name("kilogram"),
                gi=70.0
            )
        }
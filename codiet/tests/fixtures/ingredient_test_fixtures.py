"""Test fixtures for tests requiring ingredient instances."""
from typing import TYPE_CHECKING

from codiet.model.ingredients.ingredient import Ingredient

if TYPE_CHECKING:
    from codiet.tests.fixtures import UnitsTestFixtures
    from codiet.db import DatabaseService

class IngredientTestFixtures:
    """Test fixtures class for ingredients."""

    def __init__(self, units_test_fixtures:'UnitsTestFixtures') -> None:
        self._units_fixtures = units_test_fixtures

        # Initialise the ingredient class level attributes
        Ingredient.initialise_class(
            global_units=self._units_fixtures.units.values(),
            global_unit_conversions=self._units_fixtures.global_unit_conversions.values()
        )

        self._test_ingredients:dict[str, Ingredient]|None = None
        self._database_ingredients_setup:bool = False

    @property
    def ingredients(self) -> dict[str, Ingredient]:
        """Returns the test ingredients."""
        if self._test_ingredients is None:
            self._test_ingredients = self._create_ingredients()
        return self._test_ingredients
    
    def setup_database_ingredients(self, db_service:'DatabaseService') -> None:
        """Sets up the test ingredients in the database."""
        db_service.ingredients.create_ingredients(self.ingredients.values())
        self._database_ingredients_setup = True

    def _create_ingredients(self) -> dict[str, Ingredient]:
        """Instantiates a dictionary of ingredients for testing purposes."""
        return {
            "apple": Ingredient(
                name="apple",
                description="A fruit",
                cost_value=1.0,
                cost_qty_value=1.0,
                cost_qty_unit=self._units_fixtures.get_unit_by_name("kilogram"),
                gi=40.0
            ),
            "banana": Ingredient(
                name="banana",
                description="A fruit",
                cost_value=2.0,
                cost_qty_value=1.0,
                cost_qty_unit=self._units_fixtures.get_unit_by_name("kilogram"),
                gi=50.0
            ),
            "chicken": Ingredient(
                name="chicken",
                description="A meat",
                cost_value=3.0,
                cost_qty_value=1.0,
                cost_qty_unit=self._units_fixtures.get_unit_by_name("kilogram"),
                gi=60.0
            ),
            "potato": Ingredient(
                name="potato",
                description="A vegetable",
                cost_value=4.0,
                cost_qty_value=1.0,
                cost_qty_unit=self._units_fixtures.get_unit_by_name("kilogram"),
                gi=70.0
            )
        }
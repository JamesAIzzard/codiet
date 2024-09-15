"""Test fixtures for tests requiring ingredient instances."""
from typing import TYPE_CHECKING

from codiet.model.ingredients.ingredient import Ingredient

if TYPE_CHECKING:
    from codiet.tests.fixtures import UnitTestFixtures
    from codiet.db import DatabaseService

class IngredientTestFixtures:
    """Test fixtures class for ingredients."""

    def __init__(self, units_test_fixtures:'UnitTestFixtures') -> None:
        self._units_fixtures = units_test_fixtures

        # Initialise the ingredient class level attributes
        Ingredient.initialise_class(
            global_units=self._units_fixtures.units.values(),
            global_unit_conversions=self._units_fixtures.global_unit_conversions.values()
        )

        # Cache the ingredients for efficiency
        self._test_ingredients:dict[str, Ingredient]|None = None
        
        # It's useful to create a record of whether the test ingredients have been
        # set up in the database or not, for when methods depend on this.
        self._database_ingredients_setup:bool = False

    @property
    def ingredients(self) -> dict[str, Ingredient]:
        """Returns the test ingredients."""
        if self._test_ingredients is None:
            self._test_ingredients = self._build_ingredients()
        return self._test_ingredients
    
    def get_ingredient_by_name(self, ingredient_name:str) -> Ingredient:
        """Returns an ingredient by name."""
        return self.ingredients[ingredient_name]

    def setup_database_ingredients(self, db_service:'DatabaseService') -> None:
        """Sets up the test ingredients in the database."""
        db_service.ingredients.create_ingredients(self.ingredients.values())
        self._database_ingredients_setup = True

    def _build_ingredients(self) -> dict[str, Ingredient]:
        """Instantiates a dictionary of ingredients for testing purposes."""
        return {
            "apple": Ingredient(
                name="apple",
                description="A fruit",
                gi=40.0
            ),
            "chicken": Ingredient(
                name="chicken",
                description="A meat",
                gi=60.0
            ),
            "potato": Ingredient(
                name="broccoli",
                description="A vegetable",
                gi=70.0
            )
        }
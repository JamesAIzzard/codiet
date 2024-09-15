"""Test fixtures for the flags module."""
from typing import TYPE_CHECKING

from codiet.model.flags import Flag, IngredientFlag

if TYPE_CHECKING:
    from codiet.model.ingredients import Ingredient

class FlagTestFixtures:
    """Test fixtures for the flags module.
    Provides various methods to create test flags and configure test
    flags in the database.
    """

    def __init__(self) -> None:
        self._flags:dict[str, Flag]|None = None

    @property
    def flags(self) -> dict[str, Flag]:
        """Returns the test flags."""
        if self._flags is None:
            self._flags = self._create_flags()
        return self._flags

    def get_flag_by_name(self, flag_name:str) -> Flag:
        """Returns a flag by name."""
        return self.flags[flag_name]

    def create_ingredient_flag(self, flag_name:str, ingredient:'Ingredient') -> IngredientFlag:
        """Creates an ingredient flag."""
        return IngredientFlag(
            flag_name=flag_name,
            ingredient=ingredient
        )

    def _create_flags(self) -> dict[str, Flag]:
        """Instantiates a dictionary of flags for testing purposes."""
        return {
            "vegan": Flag(
                flag_name="vegan",
            ),
            "vegetarian": Flag(
                flag_name="vegetarian",
            ),
            "gluten_free": Flag(
                flag_name="gluten_free",
            ),
            "dairy_free": Flag(
                flag_name="dairy_free",
            ),
        }
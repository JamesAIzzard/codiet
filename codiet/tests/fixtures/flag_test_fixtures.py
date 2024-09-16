"""Test fixtures for the flags module."""
from typing import TYPE_CHECKING

from codiet.model.flags import Flag

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

    def _create_flags(self) -> dict[str, Flag]:
        """Instantiates a dictionary of flags for testing purposes."""
        return {
            "vegan": Flag(
                name="vegan",
            ),
            "vegetarian": Flag(
                name="vegetarian",
            ),
            "gluten_free": Flag(
                name="gluten_free",
            ),
            "dairy_free": Flag(
                name="dairy_free",
            ),
        }
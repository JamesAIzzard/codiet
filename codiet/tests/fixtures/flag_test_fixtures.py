"""Test fixtures for the flags module."""

from codiet.model.flags import Flag

class FlagTestFixtures:
    """Test fixtures for the flags module.
    Provides various methods to create test flags and configure test
    flags in the database.
    """

    def __init__(self) -> None:
        self._test_flags:dict[str, Flag]|None = None

    @property
    def flags(self) -> dict[str, Flag]:
        """Returns the test flags."""
        if self._test_flags is None:
            self._test_flags = self._create_test_flags()
        return self._test_flags

    def _create_test_flags(self) -> dict[str, Flag]:
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
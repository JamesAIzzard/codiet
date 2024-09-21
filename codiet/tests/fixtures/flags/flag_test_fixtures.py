from codiet.tests.fixtures import BaseTestFixtures
from codiet.model.flags import Flag, FlagDefinition

class FlagTestFixtures(BaseTestFixtures):

    def __init__(self) -> None:
        self._flag_definitions:dict[str, FlagDefinition]|None = None

    @property
    def flag_definitions(self) -> dict[str, FlagDefinition]:
        """Returns the test flags."""
        if self._flag_definitions is None:
            self._flag_definitions = self._create_flags_definitions()
        return self._flag_definitions

    def get_flag_definition(self, flag_name:str) -> FlagDefinition:
        """Returns a flag by name."""
        return self.flag_definitions[flag_name]

    def _create_flags_definitions(self) -> dict[str, FlagDefinition]:
        """Instantiates a dictionary of flags for testing purposes."""
        return {
            "vegan": FlagDefinition(
                flag_name="vegan",
            ),
            "vegetarian": FlagDefinition(
                flag_name="vegetarian",
            ),
            "gluten_free": FlagDefinition(
                flag_name="gluten_free",
            ),
            "dairy_free": FlagDefinition(
                flag_name="dairy_free",
            ),
        }
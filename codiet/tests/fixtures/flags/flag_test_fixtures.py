import os
from typing import TYPE_CHECKING

from codiet.utils.unique_dict import UniqueDict
from codiet.db_population.flags import FlagDefinitionJSONFetcher, JSONToFlagDefinitionFactory
from codiet.tests.fixtures import BaseTestFixture

if TYPE_CHECKING:
    from codiet.model.flags import FlagDefinition

_current_dir = os.path.dirname(__file__)
TEST_FLAG_DEFINITIONS_DATA_DIR_PATH = os.path.join(
    _current_dir, 'test_flag_definition_data'
)

class FlagTestFixtures(BaseTestFixture):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._flag_definition_json_fetcher = FlagDefinitionJSONFetcher(TEST_FLAG_DEFINITIONS_DATA_DIR_PATH)
        self._flag_definition_factory = JSONToFlagDefinitionFactory()

        self._flag_definitions = UniqueDict[str, 'FlagDefinition']()

    def get_flag_definition(self, flag_name: str) -> 'FlagDefinition':
        try:
            return self._flag_definitions[flag_name]
        except KeyError:
            flag_data = self._flag_definition_json_fetcher.fetch_data(flag_name)
            flag = self._flag_definition_factory.build(flag_name, flag_data)
            self._flag_definitions[flag_name] = flag
            return flag
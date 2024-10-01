import os
from unittest import TestCase

from codiet.data import DatabaseService, JSONRepository

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(CURRENT_DIR, "json_data")

class BaseCodietTest(TestCase):

    def setUp(self) -> None:
        super().setUp()

        test_json_repository = JSONRepository(TEST_DATA_DIR)
        DatabaseService().set_repository(test_json_repository)



import os
from unittest import TestCase

from .fixtures import OptimiserFixtures

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(CURRENT_DIR, "json_data")

class BaseCodietTest(TestCase):

    def setUp(self) -> None:
        super().setUp()

        OptimiserFixtures.reset()



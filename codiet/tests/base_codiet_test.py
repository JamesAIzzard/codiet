from unittest import TestCase

from codiet.utils import SingletonMeta

class BaseCodietTest(TestCase):
    """Base class for testing model elements."""
    
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        SingletonMeta.reset_all_instances()
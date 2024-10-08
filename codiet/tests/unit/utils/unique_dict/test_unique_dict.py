from codiet.tests import BaseCodietTest
from codiet.utils import UniqueDict

class BaseUniqueDictTest(BaseCodietTest):
    pass

class TestSetItem(BaseUniqueDictTest):
    def test_can_set_item(self):
        unique_dict = UniqueDict()
        unique_dict["key"] = "value"

        self.assertEqual(unique_dict["key"], "value")

    def test_exception_if_value_already_in_dict(self):
        unique_dict = UniqueDict()
        unique_dict["key"] = "value"

        with self.assertRaises(ValueError):
            unique_dict["key2"] = "value"
from codiet.tests import BaseCodietTest

class BaseFlagServiceTest(BaseCodietTest):
    pass

class TestMergeFlagLists(BaseFlagServiceTest):
    def test_none_overrides_other_values(self):
        flag_lists = [
            {
                "vegan": self.flag_factory.create_flag("vegan", True),
            },
            {
                "vegan": self.flag_factory.create_flag("vegan", None),
            }
        ]

        merged_flags = self.flag_service.merge_flag_lists(flag_lists)

        self.assertIsNone(merged_flags["vegan"].value)

    def test_false_overrides_true(self):
        flag_lists = [
            {
                "vegan": self.flag_factory.create_flag("vegan", True),
            },
            {
                "vegan": self.flag_factory.create_flag("vegan", False),
            }
        ]

        merged_flags = self.flag_service.merge_flag_lists(flag_lists)

        self.assertFalse(merged_flags["vegan"].value)

    def test_true_does_not_override_false(self):
        flag_lists = [
            {
                "vegan": self.flag_factory.create_flag("vegan", False),
            },
            {
                "vegan": self.flag_factory.create_flag("vegan", True),
            }
        ]

        merged_flags = self.flag_service.merge_flag_lists(flag_lists)

        self.assertFalse(merged_flags["vegan"].value)

class TestInferUndefinedFlagValues(BaseFlagServiceTest):
    def test_infer_undefined_flag_values(self):
        merged_flags = {
            "vegan": self.flag_factory.create_flag("vegan", None),
            "vegetarian": self.flag_factory.create_flag("vegetarian", None),
            "gluten_free": self.flag_factory.create_flag("gluten_free", None),
        }

        inferred_flags = self.flag_service.infer_undefined_flag_values(merged_flags)

        self.assertFalse(inferred_flags["vegan"].value)
        self.assertFalse(inferred_flags["vegetarian"].value)
        self.assertFalse(inferred_flags["gluten_free"].value)

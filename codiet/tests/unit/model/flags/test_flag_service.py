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
            },
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
            },
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
            },
        ]

        merged_flags = self.flag_service.merge_flag_lists(flag_lists)

        self.assertFalse(merged_flags["vegan"].value)


class TestInferUndefinedFlags(BaseFlagServiceTest):
    def test_infer_true_flags_from_true_value(self):
        flags = {
            "vegan": self.flag_factory.create_flag("vegan", True),
        }

        flags = self.flag_service.infer_undefined_flags(
            flags, lambda _: False
        )

        self.assertTrue(flags["vegetarian"].value)
        self.assertTrue(flags["dairy_free"].value)
        self.assertTrue(flags["pescatarian"].value)

    def test_infer_false_flags_from_false_value(self):
        flags = {
            "dairy_free": self.flag_factory.create_flag("dairy_free", False),
            "pescatarian": self.flag_factory.create_flag("pescatarian", False),
        }

        flags = self.flag_service.infer_undefined_flags(
            flags, lambda _: False
        )

        self.assertFalse(flags["vegan"].value)
        self.assertFalse(flags["vegetarian"].value)
        

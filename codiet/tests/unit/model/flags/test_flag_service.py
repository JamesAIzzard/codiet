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


class TestPopulateImpliedFlags(BaseFlagServiceTest):
    def test_implied_true_flags_are_populated_from_true_value(self):
        flags = {
            "vegan": self.flag_factory.create_flag("vegan", True),
        }

        updated_flags = self.flag_service.populate_implied_flags(flags)

        self.assertTrue(updated_flags["vegan"].value)
        self.assertTrue(updated_flags["vegetarian"].value)
        self.assertTrue(updated_flags["pescatarian"].value)

    def test_implied_true_flags_are_not_populated_from_none_value(self):
        flags = {
            "vegan": self.flag_factory.create_flag("vegan", None),
        }

        updated_flags = self.flag_service.populate_implied_flags(flags)

        self.assertIsNone(updated_flags["vegan"].value)
        self.assertIsNone(updated_flags["vegetarian"].value)
        self.assertIsNone(updated_flags["pescatarian"].value)

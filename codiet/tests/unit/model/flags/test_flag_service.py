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

    def test_none_overrides_other_values_with_multiple_flags(self):
        flag_lists = [
            {
                "vegan": self.flag_factory.create_flag("vegan", True),
                "gluten_free": self.flag_factory.create_flag("gluten_free", False),
            },
            {
                "vegan": self.flag_factory.create_flag("vegan", None),
                "gluten_free": self.flag_factory.create_flag("gluten_free", True),
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

    def test_false_overrides_true_with_multiple_flags(self):
        flag_lists = [
            {
                "vegan": self.flag_factory.create_flag("vegan", True),
                "gluten_free": self.flag_factory.create_flag("gluten_free", False),
            },
            {
                "vegan": self.flag_factory.create_flag("vegan", False),
                "gluten_free": self.flag_factory.create_flag("gluten_free", True),
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

    def test_true_does_not_override_false_with_multiple_flags(self):
        flag_lists = [
            {
                "vegan": self.flag_factory.create_flag("vegan", False),
                "gluten_free": self.flag_factory.create_flag("gluten_free", True),
            },
            {
                "vegan": self.flag_factory.create_flag("vegan", True),
                "gluten_free": self.flag_factory.create_flag("gluten_free", False),
            },
        ]

        merged_flags = self.flag_service.merge_flag_lists(flag_lists)

        self.assertFalse(merged_flags["vegan"].value)


class TestGetInferredFromFlag(BaseFlagServiceTest):
    def test_correctly_infers_flags_from_true_flag(self):
        vegan = self.flag_factory.create_flag("vegan", True)

        inferred_flags = self.flag_service.get_inferred_from_flag(
            vegan, lambda _: False
        )

        self.assertTrue(inferred_flags["vegetarian"].value)
        self.assertTrue(inferred_flags["dairy_free"].value)
        self.assertTrue(inferred_flags["pescatarian"].value)

    def test_infer_false_flags_from_false_value(self):
        vegetarian = self.flag_factory.create_flag("vegetarian", False)

        inferred_flags = self.flag_service.get_inferred_from_flag(
            vegetarian, lambda _: False
        )

        self.assertFalse(inferred_flags["vegan"].value)
        
class TestGetInferredFromFlags(BaseFlagServiceTest):
    def test_correctly_infers_flags_from_true_flags(self):
        flags = {
            "vegan": self.flag_factory.create_flag("vegan", True),
            "gluten_free": self.flag_factory.create_flag("gluten_free", True),
        }

        inferred_flags = self.flag_service.get_inferred_from_flags(
            flags, lambda _: False
        )

        self.assertTrue(inferred_flags["vegetarian"].value)
        self.assertTrue(inferred_flags["dairy_free"].value)
        self.assertTrue(inferred_flags["pescatarian"].value)

    def test_unrelated_flags_are_set_to_none(self):
        flags = {
            "vegan": self.flag_factory.create_flag("vegan", True),
            "gluten_free": self.flag_factory.create_flag("gluten_free", True),
        }

        inferred_flags = self.flag_service.get_inferred_from_flags(
            flags, lambda _: False
        )

        self.assertIsNone(inferred_flags["halal"].value)

    def test_adds_to_initially_defined_flags(self):
        flags = {
            "vegan": self.flag_factory.create_flag("vegan", True),
            "gluten_free": self.flag_factory.create_flag("gluten_free", True),
        }

        inferred_flags = self.flag_service.get_inferred_from_flags(
            flags, lambda _: False
        )

        self.assertTrue(inferred_flags["vegan"].value)
        self.assertTrue(inferred_flags["gluten_free"].value)
        self.assertTrue(inferred_flags["vegetarian"].value)
        self.assertTrue(inferred_flags["dairy_free"].value)
from codiet.tests import BaseCodietTest


class TestFlagDefinitionBase(BaseCodietTest):
    pass


class TestGetImplications(TestFlagDefinitionBase):

    def test_true_value_returns_correct_true_implications(self):
        vegan_definition = self.singleton_register.get_flag_definition("vegan")

        implied_true = vegan_definition.get_names_implied_true(True, lambda name: False)

        self.assertIn("vegetarian", implied_true)
        self.assertIn("pescatarian", implied_true)
        self.assertIn("dairy_free", implied_true)
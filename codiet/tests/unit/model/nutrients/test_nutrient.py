from codiet.tests import BaseCodietTest

class NutrientBaseTest(BaseCodietTest):
    pass

class TestIsParentOf(NutrientBaseTest):
    
    def test_returns_true_correctly(self):
        protein = self.singleton_register.get_nutrient("protein")

        self.assertTrue(protein.is_parent_of("alanine"))

    def test_returns_false_correctly(self):
        protein = self.singleton_register.get_nutrient("protein")

        self.assertFalse(protein.is_parent_of("protein"))

class TestIsChildOf(NutrientBaseTest):

    def test_returns_true_correctly(self):
        alanine = self.singleton_register.get_nutrient("alanine")

        self.assertTrue(alanine.is_child_of("protein"))

    def test_returns_false_correctly(self):
        protein = self.singleton_register.get_nutrient("protein")

        with self.assertRaises(ValueError):
            protein.is_child_of("protein")

class TestEquality(NutrientBaseTest):

    def test_equality(self):
        protein = self.singleton_register.get_nutrient("protein")
        protein2 = self.singleton_register.get_nutrient("protein")
        alanine = self.singleton_register.get_nutrient("alanine")

        self.assertEqual(protein, protein2)
        self.assertNotEqual(protein, alanine)
from codiet.tests import BaseCodietTest

class NutrientBaseTest(BaseCodietTest):
    pass

class TestName(NutrientBaseTest):

    def test_name(self):
        protein = self.singleton_register.get_nutrient("protein")
        self.assertEqual(protein.name, "protein")

    def test_cannot_set_name(self):
        protein = self.singleton_register.get_nutrient("protein")

        with self.assertRaises(AttributeError):
            protein.name = "carbohydrate" # type: ignore

class TestParent(NutrientBaseTest):
    
    def test_accessing_non_existent_parent_raises_value_error(self):
        protein = self.singleton_register.get_nutrient("protein")

        with self.assertRaises(ValueError):
            protein.parent

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
        alanine = self.singleton_register.get_nutrient("alanine")

        self.assertFalse(alanine.is_child_of("carbohydrate"))

class TestEquality(NutrientBaseTest):

    def test_equality(self):
        protein = self.singleton_register.get_nutrient("protein")
        protein2 = self.singleton_register.get_nutrient("protein")
        alanine = self.singleton_register.get_nutrient("alanine")

        self.assertEqual(protein, protein2)
        self.assertNotEqual(protein, alanine)
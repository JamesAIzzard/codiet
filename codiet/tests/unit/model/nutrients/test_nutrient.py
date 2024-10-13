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
            protein.direct_parent

    def test_returns_parent_correctly(self):
        alanine = self.singleton_register.get_nutrient("alanine")
        non_essential_amino_acid = self.singleton_register.get_nutrient("non_essential_amino_acid")

        self.assertEqual(alanine.direct_parent, non_essential_amino_acid)

class TestIsParentOf(NutrientBaseTest):
    
    def test_returns_true_correctly(self):
        protein = self.singleton_register.get_nutrient("protein")

        self.assertTrue(protein.is_parent_of("alanine"))

    def test_returns_false_correctly(self):
        protein = self.singleton_register.get_nutrient("protein")

        self.assertFalse(protein.is_parent_of("protein"))

class TestDirectChildren(NutrientBaseTest):
    
        def test_returns_children_correctly(self):
            fat = self.singleton_register.get_nutrient("fat")
            children = fat.direct_children
            self.assertEqual(len(children), 3)
            self.assertIn("saturated_fat", children)
            self.assertIn("unsaturated_fat", children)
            self.assertIn("trans_fat", children)
    
        def test_cannot_set_children(self):
            non_essential_amino_acid = self.singleton_register.get_nutrient("non_essential_amino_acid")
    
            with self.assertRaises(AttributeError):
                non_essential_amino_acid.direct_children = {} # type: ignore

            with self.assertRaises(TypeError):
                non_essential_amino_acid.direct_children["new_child"] = "new_child" # type: ignore

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
from codiet.tests import BaseCodietTest
from codiet.model.nutrients.nutrient import Nutrient, NutrientDTO

class BaseNutrientTest(BaseCodietTest):
    pass

class TestConstructor(BaseNutrientTest):

    def test_can_create_instance(self):
        nutrient = Nutrient("protein")
        self.assertIsInstance(nutrient, Nutrient)

    def test_can_create_instance_with_aliases(self):
        nutrient = Nutrient("protein", aliases=["prot"])
        self.assertIn("prot", nutrient.aliases)

    def test_raises_value_error_for_duplicate_aliases(self):
        with self.assertRaises(ValueError):
            Nutrient("protein", aliases=["prot", "prot"])

    def test_can_create_instance_with_parent(self):
        nutrient = Nutrient("sugar", parent_name="carbohydrate")
        self.assertEqual("carbohydrate", nutrient.parent_name)

    def test_can_create_instance_with_children(self):
        nutrient = Nutrient("carbohydrate", child_names=["sugar", "fibre"])
        self.assertIn("sugar", nutrient.child_names)
        self.assertIn("fibre", nutrient.child_names)

class TestFromDTO(BaseNutrientTest):

    def test_can_create_instance_from_dto(self):
        dto:'NutrientDTO' = {
            "name": "sugar",
            "aliases": ["sugars"],
            "parent_name": "carbohydrate",
            "child_names": ["simple sugar"]
        }
        nutrient = Nutrient.from_dto(dto)
        self.assertEqual("sugar", nutrient.name)
        self.assertIn("sugars", nutrient.aliases)
        self.assertEqual("carbohydrate", nutrient.parent_name)
        self.assertIn("simple sugar", nutrient.child_names)
        
class TestParent(BaseNutrientTest):

    def test_can_get_parent(self):
        nutrient = Nutrient("simple sugar", parent_name="carbohydrate")
        parent = nutrient.parent
        self.assertIsInstance(parent, Nutrient)
        self.assertEqual("carbohydrate", parent.name)

    def test_raises_value_error_for_non_child_nutrient(self):
        nutrient = Nutrient("carbohydrate")
        with self.assertRaises(ValueError):
            nutrient.parent

class TestChildren(BaseNutrientTest):
    
        def test_can_get_children(self):
            nutrient = Nutrient("carbohydrate", child_names=["simple sugar"])
            children = nutrient.children
            self.assertIn("simple sugar", children)
    
        def test_returns_empty_dict_for_non_parent_nutrient(self):
            nutrient = Nutrient("simple sugar")
            children = nutrient.children
            self.assertTrue(len(children) == 0)
from codiet.tests import BaseCodietTest

class BaseJSONRepositoryTest(BaseCodietTest):
    pass

class TestReadNutrientDTO(BaseJSONRepositoryTest):
    
    def test_reads_calorie_nutrient_correctly(self):
        protein_dto = self.json_repository.read_nutrient_dto("protein")
        self.assertEqual(protein_dto, {
            "name": "protein",
            "cals_per_gram": 4,
            "aliases": [],
            "parent_name": None,
            "child_names": ["essential amino acid", "non-essential amino acid"]
        })

    def test_reads_non_calorie_nutrient_correctly(self):
        vitamin_c_dto = self.json_repository.read_nutrient_dto("vitamin C")
        self.assertEqual(vitamin_c_dto, {
            "name": "vitamin C",
            "cals_per_gram": 0,
            "aliases": ["ascorbic acid"],
            "parent_name": "vitamins",
            "child_names": []
        })
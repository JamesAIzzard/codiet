from codiet.tests import BaseCodietTest


class BaseJSONRepositoryTest(BaseCodietTest):
    pass


class TestReadNutrientDTO(BaseJSONRepositoryTest):

    def test_reads_calorie_nutrient_correctly(self):
        protein_dto = self.json_repository.read_nutrient_dto("protein")
        self.assertEqual(
            protein_dto,
            {
                "name": "protein",
                "cals_per_gram": 4,
                "aliases": [],
                "direct_parent_name": None,
                "direct_child_names": ["essential_amino_acid", "non_essential_amino_acid"],
            },
        )

    def test_reads_non_calorie_nutrient_correctly(self):
        vitamin_c_dto = self.json_repository.read_nutrient_dto("vitamin_C")
        self.assertEqual(
            vitamin_c_dto,
            {
                "name": "vitamin_C",
                "cals_per_gram": 0,
                "aliases": ["ascorbic_acid"],
                "direct_parent_name": "vitamins",
                "direct_child_names": [],
            },
        )


class TestReadIngredientDTO(BaseJSONRepositoryTest):

    def test_returns_complete_and_correct_ingredient_dto(self):
        apple_dto = self.json_repository.read_ingredient_dto("apple")

        self.assertEqual(apple_dto["name"], "apple")
        self.assertEqual(apple_dto["description"], "A fruit that is sweet and juicy")
        self.assertEqual(
            apple_dto["unit_conversions"],
            {
                frozenset(("whole", "gram")): {
                    "from_quantity": {"unit_name": "whole", "value": 1},
                    "to_quantity": {"unit_name": "gram", "value": 182},
                }
            },
        )
        self.assertEqual(apple_dto["standard_unit"], "whole")
        self.assertEqual(
            apple_dto["quantity_cost"],
            {"quantity": {"unit_name": "whole", "value": 1}, "cost": 0.5},
        )
        self.assertEqual(
            apple_dto["flags"],
            {
                "vegan": {"name": "vegan", "value": True},
                "gluten_free": {"name": "gluten_free", "value": True},
                "vegetarian": {"name": "vegetarian", "value": True},
            },
        )
        self.assertEqual(apple_dto["gi"], 38)
        self.assertEqual(
            apple_dto["nutrient_quantities_per_gram"],
            {
                "protein": {
                    "nutrient_name": "protein",
                    "quantity": {"unit_name": "gram", "value": 0.003},
                },
                "carbohydrate": {
                    "nutrient_name": "carbohydrate",
                    "quantity": {"unit_name": "gram", "value": 0.14},
                },
                "fat": {
                    "nutrient_name": "fat",
                    "quantity": {"unit_name": "gram", "value": 0.002},
                },
                "water": {
                    "nutrient_name": "water",
                    "quantity": {"unit_name": "gram", "value": 0.85},
                },
            },
        )

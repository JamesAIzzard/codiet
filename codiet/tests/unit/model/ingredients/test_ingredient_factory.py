from codiet.tests import BaseCodietTest

class BaseIngredientFactoryTest(BaseCodietTest):
    pass

class TestCreateIngredientFromDTO(BaseCodietTest):

    def test_name_is_correct(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertEqual(ingredient.name, "apple")

    def test_description_is_correct(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertEqual(ingredient.description, "A fruit that is sweet and juicy")

    def test_unit_conversions_are_correct(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertEqual(len(ingredient.unit_conversions), 1)
        self.assertIn(frozenset(("gram", "whole")), ingredient.unit_conversions)
        gram_whole_conversion = ingredient.unit_conversions[frozenset(("gram", "whole"))]
        self.assertEqual(gram_whole_conversion.quantities["gram"].value, 182)
        self.assertEqual(gram_whole_conversion.quantities["whole"].value, 1)

    def test_gi_is_correct(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertEqual(ingredient.gi, 38)

    def test_flags_are_correct(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertEqual(len(ingredient.flags), 3)
        self.assertIn("vegan", ingredient.flags)
        self.assertIn("gluten_free", ingredient.flags)
        self.assertIn("vegetarian", ingredient.flags)

    def test_nutrient_quantities_are_correct(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertEqual(len(ingredient.nutrient_quantities_per_gram), 3)
        self.assertIn("protein", ingredient.nutrient_quantities_per_gram)
        self.assertIn("carbohydrate", ingredient.nutrient_quantities_per_gram)
        self.assertIn("fat", ingredient.nutrient_quantities_per_gram)

    def test_creates_ingredient_with_no_description(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient_dto["description"] = None
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertIsNone(ingredient.description)

    def test_creates_ingredient_with_no_gi(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient_dto["gi"] = None
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertIsNone(ingredient.gi)

    def test_creates_ingredient_with_empty_flags(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient_dto["flags"] = {}
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertEqual(len(ingredient.flags), 0)

    def test_creates_ingredient_with_empty_nutrient_quantities(self):
        ingredient_dto = self.json_repository.read_ingredient_dto("apple")
        ingredient_dto["nutrient_quantities_per_gram"] = {}
        ingredient = self.ingredient_factory.create_ingredient_from_dto(ingredient_dto)

        self.assertEqual(len(ingredient.nutrient_quantities_per_gram), 0)
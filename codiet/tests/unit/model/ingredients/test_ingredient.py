from codiet.tests import BaseModelTest
from codiet.tests.fixtures.nutrients import NutrientTestFixtures
from codiet.tests.fixtures.flags import FlagTestFixtures
from codiet.model.ingredients import Ingredient
from codiet.model.nutrients import NutrientQuantity


class BaseIngredientTest(BaseModelTest):
    """Base class for Ingredient tests."""

    def setUp(self) -> None:
        super().setUp()
        self.flag_fixtures = FlagTestFixtures.initialise()
        self.nutrient_fixtures = NutrientTestFixtures.initialise()

class TestConstructor(BaseIngredientTest):

    def test_constructor(self):
        """Checks that the ingredient can be constructed and is an instance of the Ingredient class."""
        apple = Ingredient(name="Apple")
        self.assertIsInstance(apple, Ingredient)

    def test_standard_unit_defaults_to_grams(self):
        """Test that the standard unit defaults to grams."""
        gram = self.quantities_fixtures.get_unit("gram")
        apple = Ingredient(name="Apple")
        self.assertEqual(apple.standard_unit, gram)

class TestStandardUnitProperty(BaseIngredientTest):

    def test_cant_change_standard_unit_to_unset_unit(self):
        """Check we get an exception if we try and set the standard unit to a unit
        that is not available."""
        apple = Ingredient(name="Apple")

        with self.assertRaises(ValueError):
            apple.standard_unit = self.quantities_fixtures.get_unit("millilitre")


class TestGetFlag(BaseIngredientTest):

    def test_exception_when_getting_unknown_flag(self):
        apple = Ingredient(name="Apple")

        with self.assertRaises(ValueError):
            apple.get_flag("foobar")

    def test_returns_unset_flag_with_value_none(self):
        apple = Ingredient(name="Apple")

        self.assertIsNone(apple.get_flag("vegan").value)

    def test_returns_set_flag(self):
        apple = Ingredient(name="Apple")

        apple.set_flag("vegan", True)

        self.assertTrue(apple.get_flag("vegan").value)

class TestSetFlag(BaseIngredientTest):

    def test_can_set_flag_true(self):
        apple = Ingredient(name="Apple")

        apple.set_flag("vegan", True)
        
        self.assertTrue(apple.get_flag("vegan").value)

    def test_can_set_flag_false(self):
        apple = Ingredient(name="Apple")

        apple.set_flag("vegan", False)

        self.assertFalse(apple.get_flag("vegan").value)

    def test_can_set_flag_none(self):
        apple = Ingredient(name="Apple")

        apple.set_flag("vegan", None)

        self.assertIsNone(apple.get_flag("vegan").value)

    def test_exception_when_setting_unknown_flag(self):
        apple = Ingredient(name="Apple")

        with self.assertRaises(ValueError):
            apple.set_flag("foobar", True)

class TestGetNutrientQuantity(BaseIngredientTest):

    def test_get_nutrient_quantity(self):
        """Check we can retrieve a nutrient quantity by its name."""
        apple = Ingredient(name="Apple")
        protein_quantity = self.nutrient_fixtures.create_nutrient_quantity("protein")
        apple._add_nutrient_quantity(protein_quantity)
        self.assertEqual(
            apple.get_nutrient_quantity("protein"), protein_quantity
        )

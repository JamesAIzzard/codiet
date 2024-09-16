"""Tests for the ingredient module."""

from codiet.tests.model import BaseModelTest
from codiet.model.ingredients import Ingredient
from codiet.model.nutrients import NutrientQuantity


class BaseIngredientTest(BaseModelTest):
    """Base class for Ingredient tests."""

    def setUp(self) -> None:
        super().setUp()

class TestConstructor(BaseIngredientTest):

    def test_constructor(self):
        """Checks that the ingredient can be constructed and is an instance of the Ingredient class."""
        apple = Ingredient(name="Apple")
        self.assertIsInstance(apple, Ingredient)

    def test_populates_description(self):
        """Check that the description property sets and returns correctly."""
        # Check it is set correctly when passed in the constructor
        apple = Ingredient(name="Apple", description="A fruit")
        self.assertEqual(apple.description, "A fruit")

    def test_standard_unit_defaults_to_grams(self):
        """Test that the standard unit defaults to grams."""
        gram = self.unit_fixtures.get_unit_by_name("gram")
        apple = Ingredient(name="Apple")
        self.assertEqual(apple.standard_unit, gram)

    def test_cant_init_with_unavailable_units(self):
        """Check that we get a value error if we try to initialise
        with a unit that is not available via conversions."""
        # Create an ingredient with a unit that is not available
        with self.assertRaises(ValueError):
            Ingredient(
                name="Apple",
                standard_unit=self.unit_fixtures.get_unit_by_name("millilitre"),
            )


class TestStandardUnitProperty(BaseIngredientTest):

    def test_cant_change_standard_unit_to_unset_unit(self):
        """Check we get an exception if we try and set the standard unit to a unit
        that is not available."""
        apple = Ingredient(name="Apple")

        with self.assertRaises(ValueError):
            apple.standard_unit = self.unit_fixtures.get_unit_by_name("millilitre")


class TestGetFlagByName(BaseIngredientTest):

    def test_get_flag_by_name(self):
        """Check we can retrieve a flag by its name."""
        apple = Ingredient(name="Apple")
        vegan_flag, vegetarian_flag = self._domain_service.get_flags_by_names(
            ["vegan", "vegetarian"]
        )
        apple.add_flags([vegan_flag, vegetarian_flag])

        self.assertIs(apple.get_flag_by_name("vegan"), vegan_flag)


class TestAddFlag(BaseIngredientTest):

    def test_add_flag(self):
        """Check that we can add a flag to an ingredient."""
        apple = Ingredient(name="Apple")
        vegan_flag = self._domain_service.get_flag_by_name("vegan")
        apple.add_flag(vegan_flag)

        self.assertIn(vegan_flag, apple.flags)

    def test_exception_if_adding_duplicate_flag(self):
        """Check that we get an exception if we try to add a flag that is already present."""
        apple = Ingredient(name="Apple")
        vegan_flag = self._domain_service.get_flag_by_name("vegan")
        apple.add_flag(vegan_flag)

        with self.assertRaises(ValueError):
            apple.add_flag(vegan_flag)


class TestRemoveFlag(BaseIngredientTest):

    def test_remove_flag(self):
        """Check that we can remove a flag."""
        apple = Ingredient(name="Apple")

        # Add a couple of flags to check that we only remove the one we want
        vegan_flag = self.flag_fixtures.get_flag_by_name("vegan")
        vegetarian_flag = self.flag_fixtures.get_flag_by_name("vegetarian")
        apple.add_flags([vegan_flag, vegetarian_flag])
        self.assertEqual(len(apple.flags), 2)
        apple.remove_flag(vegan_flag)
        self.assertEqual(len(apple.flags), 1)
        self.assertNotIn(vegan_flag, apple.flags)


class TestGetNutrientQuantityByName(BaseIngredientTest):

    def test_get_nutrient_quantity_by_name(self):
        """Check we can retrieve a nutrient quantity by its name."""
        apple = Ingredient(name="Apple")
        protein_quantity = NutrientQuantity(
            self._domain_service.get_nutrient_by_name("protein")
        )
        apple.add_nutrient_quantity(protein_quantity)
        self.assertEqual(
            apple.get_nutrient_quantity_by_name("protein"), protein_quantity
        )

    def test_remove_nutrient_quantities(self):
        """Check that we can remove an ingredient nutrient quantity."""
        apple = Ingredient(name="Apple")

        # Add a couple of nutrient quantities to check that we only remove the one we want
        protein_quantity = NutrientQuantity(
            self._domain_service.get_nutrient_by_name("protein")
        )
        fat_quantity = NutrientQuantity(
            self._domain_service.get_nutrient_by_name("fat")
        )
        apple.add_nutrient_quantities([protein_quantity, fat_quantity])
        self.assertEqual(len(apple.nutrient_quantities), 2)
        
        apple.remove_nutrient_quantity(protein_quantity)
        self.assertEqual(len(apple.nutrient_quantities), 1)
        self.assertNotIn(protein_quantity, apple.nutrient_quantities)
        self.assertIn(fat_quantity, apple.nutrient_quantities)

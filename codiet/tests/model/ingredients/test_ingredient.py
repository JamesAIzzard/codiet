"""Tests for the ingredient module."""

from typing import TYPE_CHECKING
from unittest import TestCase, skip

from codiet.model.ingredients import Ingredient
from codiet.model.flags import IngredientFlag
from codiet.tests.fixtures import (
    IngredientTestFixtures,
    UnitTestFixtures,
    FlagTestFixtures,
    NutrientTestFixtures,
)


class TestIngredient(TestCase):
    """Test class for the Ingredient class."""

    def setUp(self):
        self.unit_fixtures = UnitTestFixtures()
        self.flag_fixtures = FlagTestFixtures()
        self.nutrient_fixtures = NutrientTestFixtures()
        self.ingredient_fixtures = IngredientTestFixtures(
            units_test_fixtures=self.unit_fixtures
        )

    def test_constructor(self):
        """Checks that the ingredient can be constructed and is an instance of the Ingredient class."""
        apple = self.ingredient_fixtures.get_ingredient_by_name("apple")
        self.assertIsInstance(apple, Ingredient)

    def test_name(self):
        """Check the name property returns correctly."""
        apple = Ingredient(name="Apple")
        self.assertEqual(apple.name, "Apple")

    def test_description(self):
        """Check that the description property sets and returns correctly."""
        # Check it is set correctly when passed in the constructor
        apple = Ingredient(name="Apple", description="A fruit")
        self.assertEqual(apple.description, "A fruit")

        # Check we can update it
        apple.description = "A fruit that is red"
        self.assertEqual(apple.description, "A fruit that is red")

    def test_standard_unit(self):
        """Test that the standard unit defaults to grams, and that the getter and
        setter works correctly."""
        gram = self.unit_fixtures.get_unit_by_name("gram")
        kilogram = self.unit_fixtures.get_unit_by_name("kilogram")

        # Check the standard unit is grams by default
        apple = Ingredient(name="Apple")
        self.assertEqual(apple.standard_unit, gram)

        # Check we can change it
        apple.standard_unit = self.unit_fixtures.get_unit_by_name("kilogram")
        self.assertEqual(apple.standard_unit, kilogram)

    def test_cant_init_with_unavailable_units(self):
        """Check that we get a value error if we try to initialise
        with a unit that is not available via conversions."""
        # Create an ingredient with a unit that is not available
        with self.assertRaises(ValueError):
            Ingredient(
                name="Apple",
                standard_unit=self.unit_fixtures.get_unit_by_name("millilitre"),
            )

    def test_cant_change_standard_unit_to_unset_unit(self):
        """Check we get an exception if we try and set the standard unit to a unit
        that is not available."""
        apple = Ingredient(name="Apple")

        with self.assertRaises(ValueError):
            apple.standard_unit = self.unit_fixtures.get_unit_by_name("millilitre")

    @skip("Considering creating an EntityCost class")
    def test_cost_value(self):
        """Test the cost value property."""
        # Check the cost value is None to start
        self.assertIsNone(self.ingredient.cost_value)
        # Check we can set it
        self.ingredient.cost_value = 1.0
        self.assertEqual(self.ingredient.cost_value, 1.0)

    @skip("Considering creating an EntityCost class")
    def test_cost_qty_unit(self):
        """Test the cost quantity unit property."""
        # Check the cost quantity unit is the standard unit to start
        self.assertEqual(
            self.ingredient.cost_qty_unit, self.named_global_units.get_value("gram")
        )

        # Check we can update it
        self.ingredient.cost_qty_unit = self.named_global_units.get_value("kilogram")
        self.assertEqual(
            self.ingredient.cost_qty_unit, self.named_global_units.get_value("kilogram")
        )

    @skip("Considering creating an EntityCost class")
    def test_cant_change_cost_unit_to_unset_unit(self):
        """Test that we can't change the cost unit to an unset unit."""
        # Check we can't change the cost unit to an unset unit
        with self.assertRaises(ValueError):
            self.ingredient.cost_qty_unit = self.named_global_units.get_value(
                "millilitre"
            )

    @skip("Considering creating an EntityCost class")
    def test_cost_qty_value(self):
        """Test the cost quantity value property."""
        # Check the cost quantity value is None to start
        self.assertIsNone(self.ingredient.cost_qty_value)
        # Check we can set it
        self.ingredient.cost_qty_value = 1.0
        self.assertEqual(self.ingredient.cost_qty_value, 1.0)

    def test_flags(self):
        """Check that the flags property gets and sets flags correctly."""
        apple = Ingredient(name="Apple")

        # Check the flags are empty to start
        self.assertEqual(len(apple.flags), 0)

        # Check we can add a flag
        vegan_flag = self.flag_fixtures.create_ingredient_flag("vegan", apple)
        apple.add_flag(vegan_flag)
        self.assertEqual(len(apple.flags), 1)
        self.assertIn(vegan_flag, apple.flags)

    def test_gi(self):
        """Check the GI property gets and sets the GI correctly."""
        # Check it sets correctly when passed in the constructor
        apple = Ingredient(name="Apple", gi=40.0)
        self.assertEqual(apple.gi, 40.0)

        # Check we can update it
        apple.gi = 50.0
        self.assertEqual(apple.gi, 50.0)

    def test_nutrient_quantities(self):
        """Check the nutrient quantities property gets and sets nutrient quantities correctly."""
        apple = Ingredient(name="Apple")

        # Check the nutrient quantities are empty to start
        self.assertEqual(len(apple.nutrient_quantities), 0)

        # Check we can add a nutrient quantity
        protein_quantity = self.nutrient_fixtures.create_ingredient_nutrient_quantity(
            "protein", apple
        )
        apple.add_nutrient_quantity(protein_quantity)
        self.assertEqual(len(apple.nutrient_quantities), 1)

    def test_update_flags(self):
        """Test the update_flags method."""
        # Add a couple of ingredient flags
        self.ingredient.add_flags([self.ing_vegan_flag, self.ing_vegetarian_flag])

        # Check the flags are there
        self.assertIn(self.ing_vegan_flag, self.ingredient.flags)
        self.assertIn(self.ing_vegetarian_flag, self.ingredient.flags)

        # Check the values are correct
        self.assertFalse(self.ingredient.get_flag("vegan").flag_value)
        self.assertFalse(self.ingredient.get_flag("vegetarian").flag_value)

        # Create a duplicate, but with a different value
        vegan_flag_duplicate = IngredientFlag(
            ingredient=self.ingredient,
            flag=self.named_global_flags.get_value("vegan"),
            flag_value=True,
        )

        # Check we can update the flags
        self.ingredient.update_flags(vegan_flag_duplicate)

        # Check the flag is updated
        self.assertTrue(self.ingredient.get_flag("vegan").flag_value)

    def test_mutate_flag_externally(self):
        """Test that we can mutate a flag externally."""
        # Add a flag
        self.ingredient.add_flags(self.ing_vegetarian_flag)

        # Check the flag is False
        self.assertFalse(self.ingredient.get_flag("vegetarian").flag_value)

        # Mutate the flag externally
        self.ing_vegetarian_flag.flag_value = True

        # Check the flag is updated
        self.assertTrue(self.ingredient.get_flag("vegetarian").flag_value)

    def test_remove_flags(self):
        """Test the remove_flag method."""
        # Add some flags
        self.ingredient.add_flags(
            [self.ing_vegan_flag, self.ing_vegetarian_flag, self.ing_halal_flag]
        )

        # Check the flags are there
        self.assertIn(self.ing_vegan_flag, self.ingredient.flags)
        self.assertIn(self.ing_vegetarian_flag, self.ingredient.flags)
        self.assertIn(self.ing_halal_flag, self.ingredient.flags)

        # Check we can remove two of them
        self.ingredient.remove_flags([self.ing_vegan_flag, self.ing_halal_flag])

        # Check the flag is removed
        self.assertNotIn(self.ing_vegan_flag, self.ingredient.flags)
        self.assertNotIn(self.ing_halal_flag, self.ingredient.flags)
        self.assertIn(self.ing_vegetarian_flag, self.ingredient.flags)
        self.assertEqual(len(self.ingredient.flags), 1)

    def test_update_nutrient_quantities(self):
        """Test the update_nutrient_quantities method."""
        # Create a couple of nutrient quantities
        protein_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("protein"),
            nutrient_mass_unit=self.named_global_units.get_value("gram"),
            nutrient_mass_value=1,
            ingredient_grams_value=100,
        )
        fat_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("fat"),
            nutrient_mass_unit=self.named_global_units.get_value("gram"),
            nutrient_mass_value=4,
            ingredient_grams_value=100,
        )
        self.ingredient.add_nutrient_quantities([protein_quantity, fat_quantity])
        self.assertIn(protein_quantity, self.ingredient.nutrient_quantities)
        self.assertIn(fat_quantity, self.ingredient.nutrient_quantities)

        # Recreate one with an existing value to check we can update
        updated_protein_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("protein"),
            nutrient_mass_unit=self.named_global_units.get_value("gram"),
            nutrient_mass_value=2,
            ingredient_grams_value=100,
        )

        self.ingredient.update_nutrient_quantities(updated_protein_quantity)

        # Check the protein quantity is updated
        self.assertEqual(
            self.ingredient.get_nutrient_quantity("protein").nutrient_mass_value, 2
        )
        self.assertEqual(
            self.ingredient.get_nutrient_quantity("fat").nutrient_mass_value, 4
        )

    def test_remove_nutrient_quantities(self):
        """Test the remove_nutrient_quantities method."""
        # Add the nutrient quantities
        self.ingredient.add_nutrient_quantities(
            [self.protein_quantity, self.fat_quantity, self.carb_quantity]
        )

        # Check the nutrient quantities are there
        self.assertEqual(len(self.ingredient.nutrient_quantities), 3)

        # Remove two of them
        self.ingredient.remove_nutrient_quantities(
            [self.protein_quantity, self.carb_quantity]
        )

        # Check they were removed
        self.assertEqual(len(self.ingredient.nutrient_quantities), 1)
        self.assertIn(self.fat_quantity, self.ingredient.nutrient_quantities)

    def test_mutate_nutrient_quantity_externally(self):
        """Test that we can mutate a nutrient quantity externally."""
        # Add a nutrient quantity
        self.ingredient.add_nutrient_quantities(self.protein_quantity)

        # Check the nutrient quantity is there
        self.assertIn(self.protein_quantity, self.ingredient.nutrient_quantities)
        self.assertEqual(
            self.ingredient.get_nutrient_quantity("protein").nutrient_mass_value, 1
        )

        # Mutate the nutrient quantity externally
        self.protein_quantity.nutrient_mass_value = 2

        # Check this is reflected in the ingredient
        self.assertEqual(
            self.ingredient.get_nutrient_quantity("protein").nutrient_mass_value, 2
        )

    def test_adding_conversion_makes_nutrient_quantity_unit_available(self):
        """Test that adding a conversion makes the nutrient quantity unit available."""
        # Add a nutrient quantity
        self.ingredient.add_nutrient_quantities(self.protein_quantity)

        # Check we can't change the unit to an unavailable unit
        with self.assertRaises(ValueError):
            self.protein_quantity.nutrient_mass_unit = (
                self.named_global_units.get_value("millilitre")
            )

        # Add a conversion
        conversion = IngredientUnitConversion(
            ingredient=self.ingredient,
            from_unit=self.named_global_units.get_value("gram"),
            to_unit=self.named_global_units.get_value("millilitre"),
            from_unit_qty=1,
            to_unit_qty=1.2,
        )
        self.ingredient.unit_system.add_ingredient_unit_conversions(conversion)

        # Check we can now change the unit to the available unit
        self.protein_quantity.nutrient_mass_unit = self.named_global_units.get_value(
            "kilogram"
        )
        self.assertEqual(
            self.protein_quantity.nutrient_mass_unit,
            self.named_global_units.get_value("kilogram"),
        )

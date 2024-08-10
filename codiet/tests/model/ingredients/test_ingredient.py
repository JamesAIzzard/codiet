from unittest import TestCase

from codiet.utils.map import Map
from codiet.db_population.units import read_units_from_json, read_global_unit_conversions_from_json
from codiet.db_population.flags import read_global_flags_from_json
from codiet.db_population.nutrients import read_global_nutrients_from_json
from codiet.models.units.unit import Unit
from codiet.models.nutrients.nutrient import Nutrient
from codiet.models.units.ingredient_unit_conversion import IngredientUnitConversion
from codiet.models.flags.flag import Flag
from codiet.models.flags.ingredient_flag import IngredientFlag
from codiet.models.nutrients.ingredient_nutrient_quantity import IngredientNutrientQuantity
from codiet.models.ingredients.ingredient import Ingredient


class TestIngredient(TestCase):

    def setUp(self):
        # Cache the global units
        self.global_units = read_units_from_json()
        self.global_unit_conversions = read_global_unit_conversions_from_json()
        # Map the units to their names
        self.named_global_units = Map[str, Unit]()
        for global_unit in self.global_units:
            self.named_global_units.add_mapping(global_unit.unit_name, global_unit)

        # Cache the global flags
        self.global_flags = read_global_flags_from_json()
        # Map the flags to their names
        self.named_global_flags = Map[str, Flag]()
        for global_flag in self.global_flags:
            self.named_global_flags.add_mapping(global_flag.flag_name, global_flag)

        # Cache the global nutrients
        self.global_nutrients = read_global_nutrients_from_json()
        # Map the nutrients to their names
        self.named_global_nutrients = Map[str, Nutrient]()
        for global_nutrient in self.global_nutrients:
            self.named_global_nutrients.add_mapping(global_nutrient.nutrient_name, global_nutrient)

        # Create a test ingredient
        self.ingredient = Ingredient(
            name="Test Ingredient",
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions
        )

        # Create some test ingredient nutrient quantities
        self.protein_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("protein"),
            ntr_mass_unit=self.named_global_units.get_value("gram"),
            ntr_mass_value=1,
            ingredient_grams_qty=100
        )
        self.fat_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("fat"),
            ntr_mass_unit=self.named_global_units.get_value("gram"),
            ntr_mass_value=4,
            ingredient_grams_qty=100
        )
        self.carb_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("carbohydrate"),
            ntr_mass_unit=self.named_global_units.get_value("gram"),
            ntr_mass_value=3,
            ingredient_grams_qty=100
        )

    def test_name(self):
        """Test the name property."""
        # Check the ingredient instance has the correct name
        self.assertEqual(self.ingredient.name, "Test Ingredient")

    def test_description(self):
        """Test the description property."""
        # Check the description is None to start
        self.assertIsNone(self.ingredient.description)
        # Check we can set it
        self.ingredient.description = "Test Description"
        self.assertEqual(self.ingredient.description, "Test Description")

    def test_standard_unit(self):
        """Test the standard unit property."""
        # Check the standard unit is grams to start
        self.assertEqual(self.ingredient.standard_unit, self.named_global_units.get_value("gram"))

    def test_cant_init_with_unset_units(self):
        """Test that we can't initialise an ingredient without a standard unit."""
        # Check we can't initialise with unset standard unit
        with self.assertRaises(ValueError):
            Ingredient(
                name="Test Ingredient",
                global_units=self.global_units,
                global_unit_conversions=self.global_unit_conversions,
                standard_unit=self.named_global_units.get_value("millilitre")
            )
        
        # Check we can't initialise with unset cost unit
        with self.assertRaises(ValueError):
            Ingredient(
                name="Test Ingredient",
                global_units=self.global_units,
                global_unit_conversions=self.global_unit_conversions,
                cost_qty_unit=self.named_global_units.get_value("millilitre")
            )

    def test_cant_change_standard_unit_to_unset_unit(self):
        """Test that we can't change the standard unit to an unset unit."""
        # Check we can't change the standard unit to an unset unit
        with self.assertRaises(ValueError):
            self.ingredient.standard_unit = self.named_global_units.get_value("millilitre")
        
    def test_cost_value(self):
        """Test the cost value property."""
        # Check the cost value is None to start
        self.assertIsNone(self.ingredient.cost_value)
        # Check we can set it
        self.ingredient.cost_value = 1.0
        self.assertEqual(self.ingredient.cost_value, 1.0)

    def test_cost_qty_unit(self):
        """Test the cost quantity unit property."""
        # Check the cost quantity unit is the standard unit to start
        self.assertEqual(self.ingredient.cost_qty_unit, self.named_global_units.get_value("gram"))

        # Check we can update it
        self.ingredient.cost_qty_unit = self.named_global_units.get_value("kilogram")
        self.assertEqual(self.ingredient.cost_qty_unit, self.named_global_units.get_value("kilogram"))

    def test_cant_change_cost_unit_to_unset_unit(self):
        """Test that we can't change the cost unit to an unset unit."""
        # Check we can't change the cost unit to an unset unit
        with self.assertRaises(ValueError):
            self.ingredient.cost_qty_unit = self.named_global_units.get_value("millilitre")

    def test_cost_qty_value(self):
        """Test the cost quantity value property."""
        # Check the cost quantity value is None to start
        self.assertIsNone(self.ingredient.cost_qty_value)
        # Check we can set it
        self.ingredient.cost_qty_value = 1.0
        self.assertEqual(self.ingredient.cost_qty_value, 1.0)

    def test_flags(self):
        """Test the flags property."""
        # Check length of flags is 0 to start
        self.assertEqual(len(self.ingredient.flags), 0)

        # Check we can add a flag
        vegan_flag = IngredientFlag(
            ingredient=self.ingredient,
            flag_name="vegan"
        )
        self.ingredient.add_flags(vegan_flag)
        self.assertIn(vegan_flag, self.ingredient.flags)

    def test_gi(self):
        """Test the gi property."""
        # Check the gi is None to start
        self.assertIsNone(self.ingredient.gi)
        # Check we can set it
        self.ingredient.gi = 1
        self.assertEqual(self.ingredient.gi, 1)
    
    def test_nutrient_quantities(self):
        """Test the nutrient quantities property."""
        # Check the nutrient quantities are empty to start
        self.assertEqual(len(self.ingredient.nutrient_quantities), 0)

        # Check we can add a nutrient quantity and read it back with the property
        nutrient_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("protein"),
            ntr_mass_unit=self.named_global_units.get_value("gram"),
            ntr_mass_value=1,
            ingredient_grams_qty=100
        )
        self.ingredient.add_nutrient_quantities(nutrient_quantity)
        self.assertIn(nutrient_quantity, self.ingredient.nutrient_quantities)

    def test_update_flags(self):
        """Test the update_flags method."""
        # Add a couple of ingredient flags
        vegan_flag = IngredientFlag(ingredient=self.ingredient, flag_name="vegan")
        vegetarian_flag = IngredientFlag(ingredient=self.ingredient, flag_name="vegetarian")
        self.ingredient.add_flags([vegan_flag, vegetarian_flag])

        # Check the flags are there
        self.assertIn(vegan_flag, self.ingredient.flags)
        self.assertIn(vegetarian_flag, self.ingredient.flags)
        # Check the values are correct
        self.assertFalse(self.ingredient.get_flag("vegan").flag_value)
        self.assertFalse(self.ingredient.get_flag("vegetarian").flag_value)

        # Create a duplicate, but with a different value
        vegan_flag_duplicate = IngredientFlag(ingredient=self.ingredient, flag_name="vegan", flag_value=True)

        # Check we can update the flags
        self.ingredient.update_flags(vegan_flag_duplicate)

        # Check the flag is updated
        self.assertIn(vegan_flag_duplicate, self.ingredient.flags)

    def test_mutate_flag_externally(self):
        """Test that we can mutate a flag externally."""
        # Add a flag
        vegetarian_flag = IngredientFlag(ingredient=self.ingredient, flag_name="vegetarian")
        self.ingredient.add_flags(vegetarian_flag)

        # Check the flag is False
        self.assertFalse(self.ingredient.get_flag("vegetarian").flag_value)

        # Mutate the flag externally
        vegetarian_flag.flag_value = True

        # Check the flag is updated
        self.assertTrue(self.ingredient.get_flag("vegetarian").flag_value)

    def test_remove_flags(self):
        """Test the remove_flag method."""
        # Add some flags
        vegan_flag = IngredientFlag(ingredient=self.ingredient, flag_name="vegan")
        vegetarian_flag = IngredientFlag(ingredient=self.ingredient, flag_name="vegetarian")
        halal_flag = IngredientFlag(ingredient=self.ingredient, flag_name="halal")
        self.ingredient.add_flags([vegan_flag, vegetarian_flag, halal_flag])

        # Check the flags are there
        self.assertIn(vegan_flag, self.ingredient.flags)
        self.assertIn(vegetarian_flag, self.ingredient.flags)
        self.assertIn(halal_flag, self.ingredient.flags)

        # Check we can remove two of them
        self.ingredient.remove_flags([vegan_flag, halal_flag])

        # Check the flag is removed
        self.assertNotIn(vegan_flag, self.ingredient.flags)
        self.assertNotIn(halal_flag, self.ingredient.flags)
        self.assertIn(vegetarian_flag, self.ingredient.flags)
        self.assertEqual(len(self.ingredient.flags), 1)

    def test_update_nutrient_quantities(self):
        """Test the update_nutrient_quantities method."""
        # Create a couple of nutrient quantities
        protein_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("protein"),
            ntr_mass_unit=self.named_global_units.get_value("gram"),
            ntr_mass_value=1,
            ingredient_grams_qty=100
        )
        fat_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("fat"),
            ntr_mass_unit=self.named_global_units.get_value("gram"),
            ntr_mass_value=4,
            ingredient_grams_qty=100
        )        
        self.ingredient.add_nutrient_quantities([protein_quantity, fat_quantity])
        self.assertIn(protein_quantity, self.ingredient.nutrient_quantities)
        self.assertIn(fat_quantity, self.ingredient.nutrient_quantities)

        # Recreate one with an existing value to check we can update
        updated_protein_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("protein"),
            ntr_mass_unit=self.named_global_units.get_value("gram"),
            ntr_mass_value=2,
            ingredient_grams_qty=100
        )

        self.ingredient.update_nutrient_quantities(updated_protein_quantity)

        # Check the protein quantity is updated
        self.assertEqual(self.ingredient.get_nutrient_quantity("protein").ntr_mass_value, 2)
        self.assertEqual(self.ingredient.get_nutrient_quantity("fat").ntr_mass_value, 4)

    def test_remove_nutrient_quantities(self):
        """Test the remove_nutrient_quantities method."""
        # Add the nutrient quantities
        self.ingredient.add_nutrient_quantities([self.protein_quantity, self.fat_quantity, self.carb_quantity])

        # Check the nutrient quantities are there
        self.assertEqual(len(self.ingredient.nutrient_quantities), 3)

        # Remove two of them
        self.ingredient.remove_nutrient_quantities([self.protein_quantity, self.carb_quantity])

        # Check they were removed
        self.assertEqual(len(self.ingredient.nutrient_quantities), 1)
        self.assertIn(self.fat_quantity, self.ingredient.nutrient_quantities)

    def test_mutate_nutrient_quantity_externally(self):
        """Test that we can mutate a nutrient quantity externally."""
        # Add a nutrient quantity
        self.ingredient.add_nutrient_quantities(self.protein_quantity)

        # Check the nutrient quantity is there
        self.assertIn(self.protein_quantity, self.ingredient.nutrient_quantities)
        self.assertEqual(self.ingredient.get_nutrient_quantity("protein").ntr_mass_value, 1)

        # Mutate the nutrient quantity externally
        self.protein_quantity.ntr_mass_value = 2

        # Check this is reflected in the ingredient
        self.assertEqual(self.ingredient.get_nutrient_quantity("protein").ntr_mass_value, 2)

    def test_adding_conversion_makes_nutrient_quantity_unit_available(self):
        """Test that adding a conversion makes the nutrient quantity unit available."""
        # Add a nutrient quantity
        self.ingredient.add_nutrient_quantities(self.protein_quantity)

        # Check we can't change the unit to an unavailable unit
        with self.assertRaises(ValueError):
            self.protein_quantity.ntr_mass_unit = self.named_global_units.get_value("millilitre")

        # Add a conversion
        conversion = IngredientUnitConversion(
            ingredient=self.ingredient,
            from_unit=self.named_global_units.get_value("gram"),
            to_unit=self.named_global_units.get_value("millilitre"),
            from_unit_qty=1,
            to_unit_qty=1.2
        )
        self.ingredient.unit_system.add_ingredient_unit_conversions(conversion)

        # Check we can now change the unit to the available unit
        self.protein_quantity.ntr_mass_unit = self.named_global_units.get_value("kilogram")
        self.assertEqual(self.protein_quantity.ntr_mass_unit, self.named_global_units.get_value("kilogram"))

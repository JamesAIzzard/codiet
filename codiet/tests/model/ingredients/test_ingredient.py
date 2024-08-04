from unittest import TestCase

from codiet.utils.map import Map
from codiet.db_population.units import read_global_units_from_json, read_global_unit_conversions_from_json
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
        self.global_units = read_global_units_from_json()
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
        # Check the flags are empty to start
        self.assertEqual(self.ingredient.flags, set())

        # Check we can add a flag
        flag = self.named_global_flags.get_value("vegan")
        vegan_flag = IngredientFlag(
            ingredient=self.ingredient,
            flag_name="vegan"
        )
        self.ingredient.flags = set([vegan_flag])
        self.assertEqual(self.ingredient.flags, {vegan_flag})

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
        self.assertEqual(self.ingredient.nutrient_quantities, set())

        # Check we can add a nutrient quantity
        nutrient_quantity = IngredientNutrientQuantity(
            ingredient=self.ingredient,
            nutrient=self.named_global_nutrients.get_value("protein"),
            ntr_mass_unit=self.named_global_units.get_value("gram"),
            ntr_mass_value=1,
            ingredient_grams_qty=100
        )
        self.ingredient.nutrient_quantities = set([nutrient_quantity])
        self.assertEqual(self.ingredient.nutrient_quantities, {nutrient_quantity})

    def test_update_flags(self):
        """Test the update_flags method."""
        # Check the flags are empty to start
        self.assertEqual(self.ingredient.flags, set())

        # Check we can add a flag
        vegan_flag = IngredientFlag(ingredient=self.ingredient, flag_name="vegan")
        self.ingredient.update_flags(set([vegan_flag]))
        self.assertEqual(self.ingredient.flags, {vegan_flag})
        self.assertFalse(vegan_flag.flag_value)

        # Check we can add another flag
        vegetarian_flag = IngredientFlag(ingredient=self.ingredient, flag_name="vegetarian", flag_value=True)
        self.ingredient.update_flags(set([vegetarian_flag]))
        self.assertEqual(self.ingredient.flags, {vegan_flag, vegetarian_flag})

        # Check we can add another two flags, and one of them is already in the set, but has a different value
        halal_flag = IngredientFlag(ingredient=self.ingredient, flag_name="halal")
        vegan_flag = IngredientFlag(ingredient=self.ingredient, flag_name="vegan", flag_value=True)
        self.ingredient.update_flags(set([halal_flag, vegan_flag]))
        self.assertEqual(self.ingredient.flags, {halal_flag, vegan_flag, vegetarian_flag})
        # Check vegan is now true
        self.assertTrue(self.ingredient.flag_value("vegan"))

    def test_mutate_flag_externally(self):
        """Test that we can mutate a flag externally."""
        # Check the flags are empty to start
        self.assertEqual(self.ingredient.flags, set())

        # Check we can add a flag
        vegan_flag = IngredientFlag(ingredient=self.ingredient, flag_name="vegan")
        self.ingredient.update_flags(set([vegan_flag]))

        # Check the flag is there and false
        self.assertEqual(self.ingredient.flags, {vegan_flag})
        self.assertFalse(self.ingredient.flag_value("vegan"))

        # Mutate the flag externally
        vegan_flag.flag_value = True
        # Check this is reflected in the ingredient
        self.assertTrue(self.ingredient.flag_value("vegan"))
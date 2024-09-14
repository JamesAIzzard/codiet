import unittest

from codiet.db_population.units import (
    read_units_from_json,
    read_global_unit_conversions_from_json,
    name_unit_map,
)
from codiet.model.ingredients.ingredient import Ingredient
from codiet.model.ingredients.ingredient_quantity import IngredientQuantity
from codiet.model.recipes.recipe import Recipe


class TestIngredientQuantity(unittest.TestCase):
    def setUp(self) -> None:
        # Bring in the global units
        self.global_units = read_units_from_json()
        self.global_name_unit_map = name_unit_map()

        # Create a couple of test ingredients
        self.ingredient_1 = Ingredient(
            name="Test Ingredient 1",
            global_units=read_units_from_json(),
            global_unit_conversions=read_global_unit_conversions_from_json(),
        )
        self.ingredient_2 = Ingredient(
            name="Test Ingredient 2",
            global_units=read_units_from_json(),
            global_unit_conversions=read_global_unit_conversions_from_json(),
        )

        # Create a test recipe
        self.recipe = Recipe(name="Test Recipe")

        # Create a test ingredient quantity
        self.ingredient_quantity = IngredientQuantity(
            ingredient=self.ingredient_1,
            recipe=self.recipe
        )

    def test_init(self):
        # Check the ingredient quantity is the right type
        self.assertIsInstance(self.ingredient_quantity, IngredientQuantity)

    def test_ingredient(self):
        # Check the ingredient is set correctly
        self.assertEqual(self.ingredient_quantity.ingredient, self.ingredient_1)

    def test_recipe(self):
        # Check the recipe is set correctly
        self.assertEqual(self.ingredient_quantity.recipe, self.recipe)

    def test_qty_value(self):
        # Check the quantity value is None
        self.assertIsNone(self.ingredient_quantity.qty_value)

        # Set the quantity value
        self.ingredient_quantity.qty_value = 100
        # Check the quantity value is set correctly
        self.assertEqual(self.ingredient_quantity.qty_value, 100)

    def test_qty_unit(self):
        # Check the quantity unit is set correctly
        self.assertEqual(self.ingredient_quantity.qty_unit, self.ingredient_1.standard_unit)

        # Set the quantity unit to kg
        self.ingredient_quantity.qty_unit = self.global_name_unit_map.get_value("kilogram")

        # Check the quantity unit is set correctly
        self.assertEqual(self.ingredient_quantity.qty_unit, self.global_name_unit_map.get_value("kilogram"))

    def test_cant_set_qty_unit_to_unavailable_unit(self):
        # Check we can't set the quantity unit to an unavailable unit
        with self.assertRaises(ValueError):
            self.ingredient_quantity.qty_unit = self.global_name_unit_map.get_value("litre")

    def test_qty_utol(self):
        # Check the upper tolerance is None
        self.assertIsNone(self.ingredient_quantity.qty_utol)

        # Set the upper tolerance
        self.ingredient_quantity.qty_utol = 10
        # Check the upper tolerance is set correctly
        self.assertEqual(self.ingredient_quantity.qty_utol, 10)

    def test_qty_ltol(self):
        # Check the lower tolerance is None
        self.assertIsNone(self.ingredient_quantity.qty_ltol)

        # Set the lower tolerance
        self.ingredient_quantity.qty_ltol = 10
        # Check the lower tolerance is set correctly
        self.assertEqual(self.ingredient_quantity.qty_ltol, 10)

    def test_equality(self):
        # Create a couple of equal ingredient quantities
        ingredient_quantity_1 = IngredientQuantity(
            ingredient=self.ingredient_1,
            recipe=self.recipe
        )
        ingredient_quantity_2 = IngredientQuantity(
            ingredient=self.ingredient_1,
            recipe=self.recipe
        )

        # Check they are equal
        self.assertEqual(ingredient_quantity_1, ingredient_quantity_2)

        # Create a different ingredient quantity
        ingredient_quantity_3 = IngredientQuantity(
            ingredient=self.ingredient_2,
            recipe=self.recipe
        )

        # Check they are not equal
        self.assertNotEqual(ingredient_quantity_1, ingredient_quantity_3)

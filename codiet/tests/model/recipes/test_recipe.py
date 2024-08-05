import unittest
from datetime import time

from codiet.db_population.flags import read_global_flags_from_json, global_name_flag_map
from codiet.db_population.units import read_global_units_from_json, read_global_unit_conversions_from_json, global_name_unit_map
from codiet.db_population.nutrients import read_global_nutrients_from_json, global_name_nutrient_map
from codiet.db_population.tags import read_global_tags_from_json
from codiet.models.ingredients.ingredient import Ingredient
from codiet.models.ingredients.ingredient_quantity import IngredientQuantity
from codiet.models.recipes.recipe import Recipe
from codiet.models.time.recipe_serve_time_window import RecipeServeTimeWindow

class TestRecipe(unittest.TestCase):
    def setUp(self) -> None:
        # Bring in the global units
        self.global_units = read_global_units_from_json()
        self.global_unit_conversions = read_global_unit_conversions_from_json()
        self.global_name_unit_map = global_name_unit_map()

        # Bring in the nutrients
        self.global_nutrients = read_global_nutrients_from_json()
        self.global_name_nutrient_map = global_name_nutrient_map()

        # Bring in the flags
        self.global_flags = read_global_flags_from_json()
        self.global_name_flag_map = global_name_flag_map()

        # Bring in the tags
        self.global_tags = read_global_tags_from_json()

        # Create some ingredients
        self.ingredient_1 = Ingredient(
            name="Test Ingredient 1",
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions
        )
        self.ingredient_2 = Ingredient(
            name="Test Ingredient 2",
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions
        )
        self.ingredient_3 = Ingredient(
            name="Test Ingredient 3",
            global_units=self.global_units,
            global_unit_conversions=self.global_unit_conversions
        )

        # Create a recipe
        self.recipe = Recipe(name="Test Recipe")

        # Create some ingredient quantities
        self.ingredient_quantity_1 = IngredientQuantity(
            ingredient=self.ingredient_1,
            recipe=self.recipe
        )
        self.ingredient_quantity_2 = IngredientQuantity(
            ingredient=self.ingredient_2,
            recipe=self.recipe
        )
        self.ingredient_quantity_3 = IngredientQuantity(
            ingredient=self.ingredient_3,
            recipe=self.recipe
        )

        # Create some serve time windows
        self.serve_time_window_1 = RecipeServeTimeWindow(
            recipe=self.recipe,
            window=(time(8, 0), time(10, 0))
        )
        self.serve_time_window_2 = RecipeServeTimeWindow(
            recipe=self.recipe,
            window=(time(12, 0), time(14, 0))
        )

    def test_init(self):
        recipe = Recipe(name="Test Recipe")
        # Check we have a recipe instance
        self.assertIsInstance(recipe, Recipe)
        # Check the name is set correctly
        self.assertEqual(recipe.name, "Test Recipe")

    def test_cant_set_name_to_none(self):
        # Check we can't set the name to None
        with self.assertRaises(ValueError):
            self.recipe.name = None # type: ignore # Check cant set the name to None

        # Check cant set the name to empty string
        with self.assertRaises(ValueError):
            self.recipe.name = ""
        with self.assertRaises(ValueError):
            self.recipe.name = " "

    def test_use_as_ingredient(self):
        # Check the default is False
        self.assertFalse(self.recipe.use_as_ingredient)

        # Check we can set it to True
        self.recipe.use_as_ingredient = True
        self.assertTrue(self.recipe.use_as_ingredient)

        # Check we can set it to False
        self.recipe.use_as_ingredient = False
        self.assertFalse(self.recipe.use_as_ingredient)

    def test_description(self):
        # Check the default is None
        self.assertIsNone(self.recipe.description)

        # Check we can set the description
        self.recipe.description = "Test Description"
        self.assertEqual(self.recipe.description, "Test Description")

    def test_instructions(self):
        # Check the default is None
        self.assertIsNone(self.recipe.instructions)

        # Check we can set the instructions
        self.recipe.instructions = "Test Instructions"
        self.assertEqual(self.recipe.instructions, "Test Instructions")

    def test_ingredient_quantities(self):
        # Check the default is an empty list
        self.assertEqual(self.recipe.ingredient_quantities, frozenset())

        # Add a couple
        self.recipe.update_ingredient_quantities({self.ingredient_quantity_1, self.ingredient_quantity_2})

        # Check they are there
        self.assertEqual(self.recipe.ingredient_quantities, frozenset({self.ingredient_quantity_1, self.ingredient_quantity_2}))

    def test_serve_time_windows(self):
        # Check the default is an empty list
        self.assertEqual(self.recipe.serve_time_windows, frozenset())

        # Add a couple
        self.recipe.update_serve_time_windows({self.serve_time_window_1, self.serve_time_window_2})

        # Check they are there
        self.assertEqual(self.recipe.serve_time_windows, frozenset({self.serve_time_window_1, self.serve_time_window_2}))

    def test_get_ingredient_quantity(self):
        # Add a couple
        self.recipe.update_ingredient_quantities({self.ingredient_quantity_1, self.ingredient_quantity_2})

        # Check we can get them
        self.assertEqual(self.recipe.get_ingredient_quantity("Test Ingredient 1"), self.ingredient_quantity_1)
        self.assertEqual(self.recipe.get_ingredient_quantity("Test Ingredient 2"), self.ingredient_quantity_2)

        # Check we can't get one that doesn't exist
        with self.assertRaises(ValueError):
            self.recipe.get_ingredient_quantity("Test Ingredient 3")

    def test_remove_ingredient_quantities(self):
        # Add three
        self.recipe.update_ingredient_quantities({self.ingredient_quantity_1, self.ingredient_quantity_2, self.ingredient_quantity_3})

        # Remove two
        self.recipe.remove_ingredient_quantities({self.ingredient_quantity_1, self.ingredient_quantity_2})

        # Check they are gone
        self.assertEqual(self.recipe.ingredient_quantities, frozenset({self.ingredient_quantity_3}))


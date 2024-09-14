from unittest import TestCase
from datetime import time

from codiet.model.time.recipe_serve_time_window import RecipeServeTimeWindow
from codiet.model.recipes.recipe import Recipe

class TestEntityServeTimeWindow(TestCase):
    
        def setUp(self):
            # Create a test recipe
            self.recipe = Recipe(name="Test Recipe")
    
        def test_init(self):
            """Check we can initialise the object."""
            window = RecipeServeTimeWindow(recipe=self.recipe)
            # Check its the right type
            self.assertIsInstance(window, RecipeServeTimeWindow)
            # Check the window is default
            self.assertEqual(window.window, (time(0, 0), time(23, 59)))

        def test_init_with_window(self):
            """Check we can initialise the window with a window."""
            window = RecipeServeTimeWindow(recipe=self.recipe, window=(time(1, 0), time(2, 0)))
            # Check its the right type
            self.assertIsInstance(window, RecipeServeTimeWindow)
            # Check the window is correct
            self.assertEqual(window.window, (time(1, 0), time(2, 0)))

        def test_time_in_window(self):
            """Check we can check if a time is in the window."""
            window = RecipeServeTimeWindow(recipe=self.recipe, window=(time(1, 0), time(2, 0)))
            # Check the time in window method works for both times in and out of the window.
            self.assertTrue(window.time_in_window(time(1, 30)))
            self.assertFalse(window.time_in_window(time(0, 30)))

        def test_is_subset_of(self):
            """Check we can check if a window is a subset of another window."""
            window = RecipeServeTimeWindow(self.recipe, window=(time(1, 0), time(2, 0)))
            other = RecipeServeTimeWindow(self.recipe, window=(time(0, 0), time(3, 0)))
            # Check the window is a subset
            self.assertTrue(window.is_subset_of(other))
            # Check the window is not a subset
            self.assertFalse(other.is_subset_of(window))

        def test_is_superset_of(self):
            """Check we can check if a window is a superset of another window."""
            window = RecipeServeTimeWindow(self.recipe, window=(time(1, 0), time(2, 0)))
            other = RecipeServeTimeWindow(self.recipe, window=(time(0, 0), time(3, 0)))
            # Check the window is a superset
            self.assertTrue(other.is_superset_of(window))
            # Check the window is not a superset
            self.assertFalse(window.is_superset_of(other))
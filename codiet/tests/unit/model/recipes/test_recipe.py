from datetime import time

from codiet.tests import BaseCodietTest
from codiet.tests.fixtures.ingredients import IngredientTestFixtures
from codiet.model.recipes import Recipe
from codiet.model.ingredients import IngredientQuantity
from codiet.model.time import TimeWindow
from codiet.model.tags import Tag

class BaseRecipeTest(BaseCodietTest):
    
    def setUp(self) -> None:
        super().setUp()
        self.ingredient_fixtures = IngredientTestFixtures.get_instance()

class TestConstructor(BaseRecipeTest):

    def test_can_init(self):
        recipe = Recipe(name="Apple Pie")
        self.assertIsInstance(recipe, Recipe)

    def test_name_is_set(self):
        """Check the name property returns correctly."""
        # Check we get the name we passed in the constructor
        recipe = Recipe(name="Apple Pie")
        self.assertEqual(recipe.name, "Apple Pie")

class TestAddIngredientQuantity(BaseRecipeTest):

    def test_add_ingredient_quantity(self):
        """Check that an ingredient quantity can be added to the recipe."""
        recipe = Recipe(name="Apple Pie")
        self.assertEqual(len(recipe.ingredient_quantities), 0)
        apple = IngredientQuantity(self.ingredient_fixtures.create_test_ingredient("apple"))
        recipe.add_ingredient_quantity(apple)
        self.assertIn(apple, recipe.ingredient_quantities)

class TestGetIngredientQuantityByName(BaseRecipeTest):

    def test_get_ingredient_quantity_by_name(self):
        """Check that an ingredient quantity can be retrieved by its name."""
        recipe = Recipe(name="Apple Pie")

        apple_quantity = self.ingredient_fixtures.create_ingredient_quantity("apple")
        recipe.add_ingredient_quantity(apple_quantity)

        self.assertIs(recipe.get_ingredient_quantity_by_name("apple"), apple_quantity)

    def test_get_ingredient_quantity_by_name_not_found(self):
        """Check that an exception is raised when an ingredient quantity is not found."""
        recipe = Recipe(name="Apple Pie")
        with self.assertRaises(ValueError):
            recipe.get_ingredient_quantity_by_name("apple")

class TestRemoveIngredientQuantity(BaseRecipeTest):

    def test_remove_ingredient_quantity(self):
        """Check that an ingredient quantity can be removed from the recipe."""
        recipe = Recipe(name="Apple Pie")
        apple = IngredientQuantity(self.ingredient_fixtures.create_test_ingredient("apple"))
        recipe.add_ingredient_quantity(apple)
        recipe.remove_ingredient_quantity(apple)
        self.assertNotIn(apple, recipe.ingredient_quantities)

    def test_remove_ingredient_quantity_not_found(self):
        """Check that an exception is raised when an ingredient quantity is not found."""
        recipe = Recipe(name="Apple Pie")
        apple = IngredientQuantity(self.ingredient_fixtures.create_test_ingredient("apple"))
        with self.assertRaises(ValueError):
            recipe.remove_ingredient_quantity(apple)

class TestAddServeTimeWindow(BaseRecipeTest):

    def test_add_serve_time_window(self):
        """Check that a serve time window can be added to the recipe."""
        recipe = Recipe(name="Apple Pie")
        self.assertEqual(len(recipe.serve_time_windows), 0)
        breakfast = TimeWindow((time(6, 0), time(10, 0)))
        recipe.add_serve_time_window(breakfast)
        self.assertIn(breakfast, recipe.serve_time_windows)

class TestRemoveServeTimeWindow(BaseRecipeTest):

    def test_remove_serve_time_window(self):
        """Check that a serve time window can be removed from the recipe."""
        recipe = Recipe(name="Apple Pie")
        breakfast = TimeWindow((time(6, 0), time(10, 0)))
        recipe.add_serve_time_window(breakfast)
        recipe.remove_serve_time_window(breakfast)
        self.assertNotIn(breakfast, recipe.serve_time_windows)

    def test_remove_serve_time_window_not_found(self):
        """Check that an exception is raised when a serve time window is not found."""
        recipe = Recipe(name="Apple Pie")
        breakfast = TimeWindow((time(6, 0), time(10, 0)))
        with self.assertRaises(ValueError):
            recipe.remove_serve_time_window(breakfast)

class TestAddTag(BaseRecipeTest):

    def test_add_tag(self):
        """Check that a tag can be added to the recipe."""
        recipe = Recipe(name="Apple Pie")
        self.assertEqual(len(recipe.tags), 0)
        dessert = Tag("dessert")
        recipe.add_tag(dessert)
        self.assertIn(dessert, recipe.tags)

class TestRemoveTag(BaseRecipeTest):

    def test_remove_tag(self):
        """Check that a tag can be removed from the recipe."""
        recipe = Recipe(name="Apple Pie")
        dessert = Tag("dessert")
        recipe.add_tag(dessert)
        recipe.remove_tag(dessert)
        self.assertNotIn(dessert, recipe.tags)

    def test_remove_tag_not_found(self):
        """Check that an exception is raised when a tag is not found."""
        recipe = Recipe(name="Apple Pie")
        dessert = Tag("dessert")
        with self.assertRaises(ValueError):
            recipe.remove_tag(dessert)
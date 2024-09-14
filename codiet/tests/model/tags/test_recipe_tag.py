from unittest import TestCase

from codiet.model.tags.recipe_tag import RecipeTag
from codiet.model.recipes.recipe import Recipe

class TestRecipeTag(TestCase):

    def setUp(self):
        # Create a test recipe
        self.recipe = Recipe(name="Test Recipe")

    def test_init(self):
        """Test the initialisation of RecipeTag."""
        # Check we can initialise without a value
        recipe_tag = RecipeTag(
            recipe=self.recipe,
            tag_name="Test Tag"
        )
        self.assertEqual(recipe_tag.recipe, self.recipe)
        self.assertEqual(recipe_tag.tag_name, "Test Tag")
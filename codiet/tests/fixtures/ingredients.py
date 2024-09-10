"""Test fixtures related to ingredients."""

from codiet.models.ingredients.ingredient import Ingredient

def get_test_ingredients() -> dict[str, Ingredient]:
    """Create a dictionary of test ingredients."""
    return {
        "brown rice": Ingredient(
            
        )
    }
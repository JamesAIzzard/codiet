from typing import TYPE_CHECKING

from codiet.model.quantities.is_quantified import IsQuantified

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe


class RecipeQuantity(IsQuantified):

    def __init__(self, recipe: "Recipe", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._recipe = recipe

    @property
    def recipe(self) -> "Recipe":
        """Get the recipe."""
        return self._recipe

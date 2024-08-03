from typing import TYPE_CHECKING

from codiet.models.tags.tag import Tag

if TYPE_CHECKING:
    from codiet.models.recipes.recipe import Recipe

class RecipeTag(Tag):
    def __init__(
            self,
            recipe: 'Recipe',
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)

        self._recipe = recipe

    @property
    def recipe(self) -> 'Recipe':
        return self._recipe
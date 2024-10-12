from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.recipes import RecipeFactory

class RecipeFixtures:

    def __init__(self):
        self._recipe_factory: "RecipeFactory"

    def initialise(self, recipe_factory: "RecipeFactory") -> "RecipeFixtures":
        self._recipe_factory = recipe_factory
        return self
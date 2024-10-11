from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model.recipes import RecipeQuantity, RecipeFactory

class RecipeFixtures:

    def __init__(self):
        self._recipe_factory: "RecipeFactory"

    def initialise(self, recipe_factory: "RecipeFactory") -> "RecipeFixtures":
        self._recipe_factory = recipe_factory
        return self

    @property
    def porridge_500g(self) -> "RecipeQuantity":
        return self._recipe_factory.create_recipe_quantity(
            recipe_name="porridge",
            quantity_unit_name="gram",
            quantity_value=500
        )
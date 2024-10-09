from typing import TYPE_CHECKING, TypedDict

from codiet.model.quantities import IsQuantified
from codiet.model.flags import HasFlags

if TYPE_CHECKING:
    from codiet.model.quantities import QuantityDTO
    from codiet.model.flags import Flag
    from codiet.model.recipes.recipe import Recipe

class RecipeQuantityDTO(TypedDict):
    recipe_name: str
    quantity: 'QuantityDTO'

class RecipeQuantity(HasFlags, IsQuantified):

    def __init__(self, recipe:'Recipe', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._recipe = recipe
    
    @property
    def recipe(self) -> 'Recipe':
        return self._recipe

    @property
    def calories(self) -> int:
        return self.recipe.calories_per_gram * convert(self.quantity, "gram")

    def get_flag(self, flag_name: str) -> "Flag":
        return self.recipe.get_flag(flag_name)

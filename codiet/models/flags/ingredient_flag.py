from typing import TYPE_CHECKING

from .flag import Flag
if TYPE_CHECKING:
    from codiet.models.ingredients.ingredient import Ingredient

class IngredientFlag(Flag):
    """Models a flag that is associated with an ingredient."""

    def __init__(
            self,
            ingredient: 'Ingredient',
            *args, **kwargs
        ):
        """Initialise the entity flag."""
        super().__init__(*args, **kwargs)
        
        self._ingredient = ingredient

    @property
    def ingredient(self) -> 'Ingredient':
        """Returns the ingredient associated with the flag."""
        return self._ingredient

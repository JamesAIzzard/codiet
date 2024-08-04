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
    def flag_value(self) -> bool:
        """Get the value of the flag."""
        return super().flag_value

    @flag_value.setter
    def flag_value(self, value: bool):
        """Set the value of the flag with additional checks on the ingredient."""
        # Perform any checks on the ingredient here
        # For example:
        # if self._ingredient.some_condition:
            # Handle the condition
            # pass

        # Call the parent class's setter
        super(IngredientFlag, self.__class__).flag_value.fset(self, value)

    @property
    def ingredient(self) -> 'Ingredient':
        """Returns the ingredient associated with the flag."""
        return self._ingredient

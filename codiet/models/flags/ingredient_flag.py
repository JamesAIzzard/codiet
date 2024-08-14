from typing import TYPE_CHECKING

from .flag import Flag

if TYPE_CHECKING:
    from codiet.models.ingredients.ingredient import Ingredient

class IngredientFlag(Flag):
    """Models a flag that is associated with an ingredient."""

    def __init__(
            self,
            ingredient: 'Ingredient',
            flag: Flag,
            flag_value: bool = False,
            *args, **kwargs
        ):
        """Initialize the ingredient flag."""
        super().__init__(flag_name=flag.flag_name, *args, **kwargs)
        
        self._ingredient = ingredient
        self._flag = flag
        self._flag_value = flag_value

    @property
    def flag_value(self) -> bool:
        """Get the value of the flag."""
        return self._flag_value

    @flag_value.setter
    def flag_value(self, value: bool):
        """Set the value of the flag with additional checks on the ingredient."""
        # Perform any checks on the ingredient here
        # For example:
        # if self._ingredient.some_condition:
        #     # Handle the condition
        #     pass

        self._flag_value = value

    @property
    def flag(self) -> Flag:
        """Returns the flag associated with the ingredient flag."""
        return self._flag

    @property
    def ingredient(self) -> 'Ingredient':
        """Returns the ingredient associated with the flag."""
        return self._ingredient
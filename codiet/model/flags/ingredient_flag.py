"""Defines the ingredient flag class."""

from typing import TYPE_CHECKING

from codiet.model.flags import Flag

if TYPE_CHECKING:
    from codiet.model.ingredients import Ingredient

class IngredientFlag(Flag):
    """Extends the flag class to associate it with an ingredient."""

    def __init__(
            self,
            ingredient: 'Ingredient',
            value: bool|None = None,
            *args, **kwargs
        ):
        """Initialise the ingredient flag."""
        # Since we accept the global flag instance, we need to 
        # pass the flag name to the parent class
        super().__init__(*args, **kwargs)
        
        self._ingredient = ingredient
        self.flag_value = value

    @property
    def flag_value(self) -> bool|None:
        """Get the flag value."""
        return self._flag_value
    
    @flag_value.setter
    def flag_value(self, value: bool|None):
        """Set the flag value."""
        if not self.can_have_value(value):
            raise ValueError(f"Flag {self.flag_name} cannot have value {value}.")
        self._flag_value = value

    @property
    def ingredient(self) -> 'Ingredient':
        """Returns the ingredient id associated with the flag."""
        return self._ingredient
    
    def can_have_value(self, value: bool|None) -> bool:
        """Check if the flag can have the given value."""
        return True
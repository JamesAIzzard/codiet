"""Defines the ingredient flag class."""

from .flag import Flag

class IngredientFlag(Flag):
    """Extends the flag class to associate it with an ingredient."""

    def __init__(
            self,
            global_flag_id: int,
            ingredient_id: int,
            *args, **kwargs
        ):
        """Initialise the ingredient flag."""
        super().__init__(*args, **kwargs)
        
        self._global_flag_id = global_flag_id
        self._ingredient_id = ingredient_id

    @property
    def global_flag_id(self) -> int:
        """Get the global flag ID."""
        return self._global_flag_id

    @Flag.flag_value.setter
    def flag_value(self, value: bool):
        """Set the value of the flag with additional checks on the ingredient."""
        
        # Perform any checks on the ingredient here

        # Call flag value on the superclass
        super().flag_value = value

    @property
    def ingredient_id(self) -> int:
        """Returns the ingredient id associated with the flag."""
        return self._ingredient_id
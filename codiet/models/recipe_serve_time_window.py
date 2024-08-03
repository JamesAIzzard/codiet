from typing import TYPE_CHECKING
from datetime import time

from codiet.db.stored_entity import StoredEntity

if TYPE_CHECKING:
    from codiet.models.recipes.recipe import Recipe

class RecipeServeTimeWindow(StoredEntity):
    def __init__(
            self,
            recipe: 'Recipe',
            window: tuple[time, time]|None = None,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)

        self.__recipe = recipe
        self._window = window if window is not None else (time(0, 0), time(23, 59))
    
    @property
    def recipe(self) -> 'Recipe':
        return self.__recipe

    @property
    def window(self) -> tuple[time, time]:
        return self._window
    
    @window.setter
    def window(self, window: tuple[time, time]) -> None:
        self._window = window

    def time_in_window(self, time: time) -> bool:
        """Check if the time is within the window."""
        return self._window[0] <= time <= self._window[1]
    
    def is_subset_of(self, other: 'RecipeServeTimeWindow') -> bool:
        """Check if the window is a subset of another window."""
        return other._window[0] <= self._window[0] and other._window[1] >= self._window[1]
    
    def is_superset_of(self, other: 'RecipeServeTimeWindow') -> bool:
        """Check if the window is a superset of another window."""
        return self._window[0] <= other._window[0] and self._window[1] >= other._window[1]
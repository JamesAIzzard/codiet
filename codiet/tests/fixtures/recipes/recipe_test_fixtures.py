from typing import TYPE_CHECKING

from .create_test_recipes import create_apple_pie

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe

class RecipeTestFixtures:
    
    def __init__(self) -> None:
        self._apple_pie = None
    
    @property
    def apple_pie(self) -> 'Recipe':
        if self._apple_pie is None:
            self._apple_pie = create_apple_pie()
        return self._apple_pie
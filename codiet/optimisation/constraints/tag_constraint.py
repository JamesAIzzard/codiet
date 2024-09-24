from typing import TYPE_CHECKING

from .constraint import Constraint

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe

class TagConstraint(Constraint):
    def __init__(self, tag_name:str):
        self._tag_name = tag_name

    def is_satisfied(self, recipe:'Recipe') -> bool:
        return self._tag_name in recipe.tags
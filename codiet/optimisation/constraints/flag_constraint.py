from typing import TYPE_CHECKING

from .constraint import Constraint

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe

class FlagConstraint(Constraint):
    def __init__(self, flag_name:str, value:bool|None):
        self.flag_name = flag_name
        self.value = value

    def is_satisfied(self, recipe:'Recipe') -> bool:
        return recipe.get_flag(self.flag_name).value == self.value
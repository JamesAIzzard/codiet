from typing import TYPE_CHECKING

from codiet.model.flags import Flag
from .. import TreeNode
from ..problems import Problem

if TYPE_CHECKING:
    from codiet.model.recipes import Recipe

class Solution(TreeNode['Problem']):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._recipe:Recipe|None = None

    @property
    def recipe(self) -> 'Recipe':
        if self._recipe is None:
            raise ValueError('Recipe has not been set')
        return self._recipe

    def get_flag(self, name: str) -> Flag:
        raise NotImplementedError
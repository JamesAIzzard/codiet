from typing import TYPE_CHECKING
from codiet.utils import IUC, MUC
from ..tree_node import TreeNode, DictStructure

if TYPE_CHECKING:
    from ..constraints import Constraint
    from ..goals import Goal

class Problem(TreeNode):
    def __init__(self, structure:DictStructure|None = None, *args, **kwargs):
        super().__init__(structure, *args, **kwargs)
        
        self._constraints = MUC['Constraint']()
        self._goals = MUC['Goal']()

    def _create_child(self, value: DictStructure) -> 'Problem':
        return Problem(value)

    @property
    def constraints(self) -> IUC['Constraint']:
        return self._constraints.immutable

    def add_constraint(self, constraint: 'Constraint'):
        self._constraints.add(constraint)

    def add_goal(self, goal: 'Goal'):
        self._goals.add(goal)
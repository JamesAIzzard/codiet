from typing import TYPE_CHECKING, Type

from ..tree_node import TreeNode

if TYPE_CHECKING:
    from ..constraints import Constraint
    from ..goals import Goal

class Problem(TreeNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._constraints: list[Constraint] = []
        self._goals: list[Goal] = []

    def add_constraint(self, constraint: 'Constraint'):
        self._constraints.append(constraint)

    def add_goal(self, goal: 'Goal'):
        self._goals.append(goal)
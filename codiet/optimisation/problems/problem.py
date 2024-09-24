from typing import TYPE_CHECKING
from codiet.utils import IUC, MUC
from .. import TreeNode

if TYPE_CHECKING:
    from ..constraints import Constraint
    from ..goals import Goal

class Problem(TreeNode['Problem']):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._constraints = MUC['Constraint']()
        self._goals = MUC['Goal']()

    @property
    def constraints(self) -> IUC['Constraint']:
        return self._constraints.immutable

    def add_constraint(self, constraint: 'Constraint'):
        self._constraints.add(constraint)

    def add_goal(self, goal: 'Goal'):
        self._goals.add(goal)
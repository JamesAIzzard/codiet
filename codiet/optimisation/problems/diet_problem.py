from typing import TYPE_CHECKING

from collections import UserDict
from codiet.utils import IUC, MUC

if TYPE_CHECKING:
    from codiet.optimisation.constraints import Constraint
    from codiet.optimisation.goals import Goal

class DietProblem(UserDict):
    def __init__(self, name: str, structure: dict[str, dict] | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._name = name
        
        self._constraints = MUC['Constraint']()
        self._goals = MUC['Goal']()
        
        if structure:
            self.data = {k: DietProblem(k, v) if v is not None else DietProblem(k) for k, v in structure.items()}

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def constraints(self) -> IUC['Constraint']:
        return self._constraints.immutable
    
    @property
    def goals(self) -> IUC['Goal']:
        return self._goals.immutable

    def add_subproblem(self, name: str, structure: dict[str, dict] | None = None) -> 'DietProblem':
        self.data[name] = DietProblem(name, structure)
        return self

    def add_constraint(self, constraint: 'Constraint') -> 'DietProblem':
        self._constraints.append(constraint)
        return self

    def add_goal(self, goal: 'Goal') -> 'DietProblem':
        self._goals.append(goal)
        return self

    def is_leaf(self) -> bool:
        return len(self.data) == 0
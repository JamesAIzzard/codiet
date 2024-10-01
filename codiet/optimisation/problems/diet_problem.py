from typing import TYPE_CHECKING
from codiet.utils import IUC, MUC
from codiet.optimisation.diet_structure import DietStructure

if TYPE_CHECKING:
    from codiet.optimisation.constraints import Constraint
    from codiet.optimisation.goals import Goal

class DietProblem(DietStructure):
    def __init__(self, name: str, structure: dict[str, dict] | None = None, parent: 'DietProblem|None' = None, *args, **kwargs):
        super().__init__(name, parent, *args, **kwargs)
        
        self._constraints = MUC['Constraint']()
        self._goals = MUC['Goal']()
        
        if structure:
            self.data = {k: DietProblem(k, v, parent=self) if v is not None else DietProblem(k, parent=self) for k, v in structure.items()}

    @property
    def constraints(self) -> IUC['Constraint']:
        return self._constraints.immutable
    
    @property
    def goals(self) -> IUC['Goal']:
        return self._goals.immutable

    def add_subproblem(self, name: str, structure: dict[str, dict] | None = None) -> 'DietProblem':
        self.data[name] = DietProblem(name, structure, parent=self)
        return self

    def add_constraint(self, constraint: 'Constraint') -> 'DietProblem':
        self._constraints.append(constraint)
        return self

    def add_goal(self, goal: 'Goal') -> 'DietProblem':
        self._goals.append(goal)
        return self

    def get_all_constraints(self) -> list['Constraint']:
        all_constraints = list(self.constraints)
        current = self._parent
        while current is not None:
            all_constraints.extend(current.constraints) # type: ignore
            current = current._parent
        return all_constraints
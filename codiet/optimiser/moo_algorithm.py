from abc import ABC, abstractmethod

class MOOAlgorithm(ABC):
    """Models the multi-objective optimisation algorithm."""

    @abstractmethod
    def solve(self, problem:'DietOptimisationProblem') -> 'DietSolutionSet':
        """Solve the specified problem."""
        raise NotImplementedError("Method not implemented.")
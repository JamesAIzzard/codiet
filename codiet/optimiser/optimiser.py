"""Defines the main optimisation class, responsible for using the optimiser to find the Pareto front of solutions."""

from codiet.utils import IUC

class Optimiser:
    """Models the optimiser.
    Responsible for applying the algorithm to find the Pareto front of meal plans
    for the given constraints and objectives.
    """

    def __init__(self):
        """Initialises the class."""

    def solve(self, problem:'MOOProblem', algorithm:'MOOAlgorithm') -> IUC['MealPlan']:
        """Solve the specified problem with the specified algorithm."""
        raise NotImplementedError("Method not implemented.")
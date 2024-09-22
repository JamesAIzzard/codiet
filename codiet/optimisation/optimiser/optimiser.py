from codiet.utils import IUC
from codiet.model import DietPlan

class Optimiser:

    def solve(self) -> IUC['DietPlan']:
        return IUC([DietPlan()])
        
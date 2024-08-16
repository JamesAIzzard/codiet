import numpy as np
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.optimize import minimize
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.scatter import Scatter
from .utils import solve

# Create reference directions
ref_dirs = get_reference_directions("das-dennis", 2, n_partitions=12)

# Create the NSGA-III algorithm
algorithm = NSGA3(
    pop_size=92,
    ref_dirs=ref_dirs
)

# Define the constraints
con_1 = "vegetarian"
con_2 = "gluten_free"
con_3 = "nut_free"
constraints = [con_1, con_2, con_3]

# Define the goals
goal_1 = "minimise_cost"
goal_2 = ("protein_perc", 0.3)
goal_3 = ("carb_perc", 0.4)
goal_4 = ("fat_perc", 0.3)
goals = [goal_1, goal_2, goal_3, goal_4]

# Solve the optimisation problem
solve(constraints, goals, algorithm)
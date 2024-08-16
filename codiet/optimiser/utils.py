from pymoo.problems import get_problem
from pymoo.visualization.scatter import Scatter
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def codiet_alg_main():
    return get_problem("kursawe")

def format_results(res):
    # Number of points in each axis
    num_points = 4

    # Generate grid of x and y values
    x = np.linspace(-1, -0.4, num_points)
    y = np.linspace(-0.4, 0.2, num_points)
    x, y = np.meshgrid(x, y)

    # Define the surface, e.g., a paraboloid z = x^2 + y^2
    z = x**2 + y**2

    # Flatten the arrays for the scatter plot
    x_flat = x.flatten()
    y_flat = y.flatten()
    z_flat = z.flatten()

    # Generate random colors based on a temperature scale
    colors = cm.hot(np.random.rand(num_points * num_points))

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x_flat, y_flat, z_flat, c=colors, marker='o')

    # Set labels
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # Show the plot
    plt.show()

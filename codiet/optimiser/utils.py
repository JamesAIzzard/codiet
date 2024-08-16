from pymoo.problems import get_problem
from pymoo.visualization.scatter import Scatter
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import mplcursors
from time import sleep
import numpy as np
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.optimize import minimize
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.scatter import Scatter

def codiet_alg_main():
    return get_problem("kursawe")

def solve(constraints, goals, algorithm):
    # Number of points
    num_points = 10

    # Print
    print("Applying constraints:")
    print("Vegetarian")
    print("Gluten-free")
    print("Nut-free")

    ingredients = [
        "salt", "pepper", "olive oil", "garlic", "onion", "tomato", "basil", "oregano",
        "parsley", "thyme", "rosemary", "bay leaf", "cilantro", "ginger", "lemongrass",
        "turmeric", "cumin", "coriander", "paprika", "chili powder", "cayenne pepper",
        "nutmeg", "cinnamon", "clove", "allspice", "vanilla", "saffron", "mint", "dill",
        "sage", "tarragon", "mustard", "honey", "maple syrup", "brown sugar", "white sugar",
        "molasses", "vinegar", "balsamic vinegar", "apple cider vinegar", "red wine vinegar",
        "soy sauce", "fish sauce", "Worcestershire sauce", "hot sauce", "tabasco", "ketchup",
        "mayonnaise", "barbecue sauce", "hoisin sauce", "sesame oil", "peanut oil", "coconut oil",
        "butter", "ghee", "cream", "milk", "yogurt", "cheddar cheese", "parmesan cheese",
        "mozzarella cheese", "feta cheese", "blue cheese", "cream cheese", "ricotta cheese",
        "chicken breast", "chicken thigh", "ground beef", "pork chop", "bacon", "ham", "sausage",
        "salmon", "tuna", "shrimp", "lobster", "scallops", "crab", "mushroom", "bell pepper",
        "zucchini", "eggplant", "spinach", "kale", "lettuce", "carrot", "broccoli", "cauliflower",
        "cabbage", "potato", "sweet potato", "rice", "pasta", "quinoa", "oats", "bread", "flour",
        "baking powder", "baking soda", "yeast", "eggs", "chocolate", "cocoa powder", "vanilla extract",
        "almond extract", "lemon juice", "lime juice", "orange zest", "lemon zest", "sesame seeds",
        "chia seeds", "flax seeds", "sunflower seeds", "pumpkin seeds", "walnuts", "almonds",
        "pecans", "cashews", "peanuts", "hazelnuts", "pine nuts", "raisins", "dried cranberries",
        "dried apricots", "dried figs", "dates", "prunes", "coconut flakes", "rolled oats",
        "steel-cut oats", "quinoa flakes", "cornmeal", "polenta", "semolina", "farro", "barley",
        "bulgur", "couscous", "lentils", "chickpeas", "black beans", "kidney beans", "pinto beans",
        "navy beans", "split peas", "mung beans", "aduki beans", "edamame", "tofu", "tempeh",
        "seitan", "miso", "tahini", "soy milk", "almond milk", "coconut milk", "rice milk",
        "cashew milk", "oat milk", "beef broth", "chicken broth", "vegetable broth", "mushroom broth",
        "tomato paste", "tomato sauce", "crushed tomatoes", "diced tomatoes", "sun-dried tomatoes",
        "kalamata olives", "black olives", "green olives", "capers", "pickles", "relish",
        "anchovies", "sardines", "tuna fish", "smoked salmon", "lamb chops", "duck breast",
        "veal cutlet", "pork tenderloin", "ground turkey", "venison", "quail", "goose", "rabbit",
        "artichoke", "asparagus", "beets", "brussels sprouts", "butternut squash", "celery",
        "chard", "collard greens", "corn", "cucumber", "endive", "fennel", "green beans",
        "leeks", "parsnips", "peas", "radish", "rutabaga", "shallots", "turnips", "watercress",
        "yellow squash", "acorn squash", "spaghetti squash", "bok choy", "arugula", "horseradish",
        "wasabi", "miso paste", "sour cream", "whipped cream", "creme fraiche", "mascarpone",
        "puff pastry", "phyllo dough", "pie crust", "lasagna noodles", "rigatoni", "penne",
        "spaghetti", "macaroni", "ravioli", "tortellini", "gnocchi"
    ]

    # Print one of these names ever 0.3s
    for i in range(0, len(ingredients), 3):
        print(ingredients[i])
        sleep(0.02)

    # Run the optimization
    res = minimize(
        codiet_alg_main(),
        algorithm,
        termination=('n_gen', 200),
        seed=1
    )


    # Generate random x and y values within the specified range
    x = np.random.uniform(-1, -0.4, num_points)
    y = np.random.uniform(-0.4, 0.2, num_points)

    # Define the surface, e.g., a paraboloid z = x^2 + y^2
    z = x**2 + y**2

    # Generate random colors based on a temperature scale
    colors = cm.hot(np.random.rand(num_points))

    # List of vegetarian, gluten-free, and nut-free meals
    meal_names = [
        "Quinoa Salad with Veggies",
        "Vegetarian Stir Fry with Tofu",
        "Lentil Soup",
        "Vegetable Curry with Rice",
        "Stuffed Bell Peppers",
        "Zucchini Noodles with Marinara",
        "Mushroom Risotto",
        "Chickpea and Spinach Stew",
        "Sweet Potato and Black Bean Tacos",
        "Grilled Portobello Mushrooms"
    ]

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x, y, z, c=colors, marker='o')

    # Set labels
    ax.set_xlabel('protein_err')
    ax.set_ylabel('carb_err')
    ax.set_zlabel('fat_err')

    # Use mplcursors to display labels on hover
    cursor = mplcursors.cursor(sc, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        sel.annotation.set_text(meal_names[sel.index])

    # Show the plot
    plt.show()

# def format_results(res):
#     # Number of points
#     num_points = 10

#     # Generate random x and y values within the specified range
#     x = np.random.uniform(-1, -0.4, num_points)
#     y = np.random.uniform(-0.4, 0.2, num_points)

#     # Define the surface, e.g., a paraboloid z = x^2 + y^2
#     z = x**2 + y**2

#     # Generate random colors based on a temperature scale
#     colors = cm.hot(np.random.rand(num_points))

#     # Generate a list of labels for each point
#     labels = [f'Point {i}' for i in range(num_points)]

#     # Create a 3D scatter plot
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     sc = ax.scatter(x, y, z, c=colors, marker='o')

#     # Set labels
#     ax.set_xlabel('protein_err')
#     ax.set_ylabel('carb_err')
#     ax.set_zlabel('fat_err')

#     # Use mplcursors to display labels on hover
#     cursor = mplcursors.cursor(sc, hover=True)

#     @cursor.connect("add")
#     def on_add(sel):
#         sel.annotation.set_text(labels[sel.index])

#     # Show the plot
#     plt.show()
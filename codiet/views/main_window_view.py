from PyQt6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QMenu,
    QStackedWidget,
    QWidget
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import pyqtSignal

class MainWindowView(QMainWindow):
    """The main window view for the CoDiet application."""
    # Define signals
    newIngredientClicked = pyqtSignal()
    editIngredientClicked = pyqtSignal()
    deleteIngredientClicked = pyqtSignal()
    newRecipeClicked = pyqtSignal()
    editRecipeClicked = pyqtSignal()
    editRecipeTypesClicked = pyqtSignal()
    deleteRecipeClicked = pyqtSignal()
    newGoalSetClicked = pyqtSignal()
    solveGoalSetClicked = pyqtSignal()
    editGoalSetClicked = pyqtSignal()
    deleteGoalSetClicked = pyqtSignal()
    viewResultClicked = pyqtSignal()
    editGoalDefaultsClicked = pyqtSignal()
    generalHelpClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("CoDiet - Computational Nutrition")
        # Set the window size
        self.resize(900, 600)
        # Set the window icon
        icon = QIcon("codiet/resources/icons/app-icon.png")
        self.setWindowIcon(icon)

        # Build the menu bar
        self._build_menu_bar()

        # Create a dict for the individual pages
        self.pages = {}
        # Create a stacked widget to hold the pages
        self._page_stack = QStackedWidget()
        self.setCentralWidget(self._page_stack)

    def add_page(self, name: str, page):
        """Adds a page to the stacked widget."""
        self.pages[name] = page
        self._page_stack.addWidget(page)

    def show_page(self, name: str):
        """Shows the page with the given name."""
        self._page_stack.setCurrentWidget(self.pages[name])

    def _build_menu_bar(self):
        # Create a menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Create the Ingredients menu
        ingredients_menu = QMenu("Ingredients", self)
        menu_bar.addMenu(ingredients_menu)
        # Create the "New Ingredient" action
        self.new_ingredient_action = QAction("New Ingredient", self)
        ingredients_menu.addAction(self.new_ingredient_action)
        self.new_ingredient_action.triggered.connect(self.newIngredientClicked.emit)
        # Create the "Edit Ingredient" action
        self.edit_ingredient_action = QAction("Edit Ingredient", self)
        ingredients_menu.addAction(self.edit_ingredient_action)
        self.edit_ingredient_action.triggered.connect(self.editIngredientClicked.emit)
        # Create a "Delete Ingredient" action
        self.delete_ingredient_action = QAction("Delete Ingredient", self)
        ingredients_menu.addAction(self.delete_ingredient_action)
        self.delete_ingredient_action.triggered.connect(self.deleteIngredientClicked.emit)


        # Create the Recipes menu
        recipes_menu = QMenu("Recipes", self)
        menu_bar.addMenu(recipes_menu)
        # Create the "New Recipe" action
        self.new_recipe_action = QAction("New Recipe", self)
        recipes_menu.addAction(self.new_recipe_action)
        self.new_recipe_action.triggered.connect(self.newRecipeClicked.emit)
        # Create the "Edit Recipe" action
        self.edit_recipe_action = QAction("Edit Recipe", self)
        recipes_menu.addAction(self.edit_recipe_action)
        self.edit_recipe_action.triggered.connect(self.editRecipeClicked.emit)
        # Create an "Edit Recipe Types" action
        self.edit_recipe_types_action = QAction("Edit Recipe Types", self)
        recipes_menu.addAction(self.edit_recipe_types_action)
        self.edit_recipe_types_action.triggered.connect(self.editRecipeTypesClicked.emit)
        # Create a "Delete Recipe" action
        self.delete_recipe_action = QAction("Delete Recipe", self)
        recipes_menu.addAction(self.delete_recipe_action)
        self.delete_recipe_action.triggered.connect(self.deleteRecipeClicked.emit)

        # Create the Nutritional Solver menu
        solver_menu = QMenu("Meal Planner", self)
        menu_bar.addMenu(solver_menu)

        # Create the Results Menu
        results_menu = QMenu("Results", self)
        menu_bar.addMenu(results_menu)

        # Create the Preferences menu
        preferences_menu = QMenu("Preferences", self)
        menu_bar.addMenu(preferences_menu)
        # Add a set meal goal defaults action
        self.edit_goal_defaults_action = QAction("Edit Meal Goal Defaults", self)
        preferences_menu.addAction(self.edit_goal_defaults_action)
        self.edit_goal_defaults_action.triggered.connect(self.editGoalDefaultsClicked.emit)

        # Create the Help menu
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)
        self.general_help_action = QAction("General Help", self)
        help_menu.addAction(self.general_help_action)
        self.general_help_action.triggered.connect(self.generalHelpClicked.emit)

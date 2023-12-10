from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QStackedWidget, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QAction, QIcon

from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.recipe_editor_view import RecipeEditorView

class MainWindowView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("CoDiet - Computational Nutrition")

        # Set the window size
        self.resize(900, 600)

        # Set the window icon   
        icon = QIcon('codiet/resources/icons/icon.png')
        self.setWindowIcon(icon)

        # Build the menu bar
        self._build_menu_bar()

        # Create a stacked widget to hold the pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        # Create the pages for the stacked widget
        self.ingredient_editor_view = IngredientEditorView()
        self.recipe_editor_view = RecipeEditorView()
        # Add the pages to the stacked widget
        self.stacked_widget.addWidget(self.ingredient_editor_view)
        self.stacked_widget.addWidget(self.recipe_editor_view)    

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
        # Create the "Edit Ingredient" action
        self.edit_ingredient_action = QAction("Edit Ingredient", self)
        ingredients_menu.addAction(self.edit_ingredient_action)

        # Create the Recipes menu
        recipes_menu = QMenu("Recipes", self)
        menu_bar.addMenu(recipes_menu)
        # Create the "New Recipe" action
        self.new_recipe_action = QAction("New Recipe", self)
        recipes_menu.addAction(self.new_recipe_action)
        # Create the "Edit Recipe" action
        self.edit_recipe_action = QAction("Edit Recipe", self)
        recipes_menu.addAction(self.edit_recipe_action)

        # Create the Meal Goals menu
        meal_goals_menu = QMenu("Meal Goals", self)
        menu_bar.addMenu(meal_goals_menu)

        # Create the Day Plans menu
        day_plans_menu = QMenu("Day Plans", self)
        menu_bar.addMenu(day_plans_menu)

        # Create the Run menu
        run_menu = QMenu("Run", self)
        menu_bar.addMenu(run_menu)

        # Create the Preferences menu
        preferences_menu = QMenu("Preferences", self)
        menu_bar.addMenu(preferences_menu)

        # Create the Help menu
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)

    def show_ingredient_editor(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_recipe_editor(self):
        self.stacked_widget.setCurrentIndex(1)
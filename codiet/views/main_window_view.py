from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QStackedWidget, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QAction, QIcon

from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.ingredient_search_popup_view import IngredientSearchPopupView
from codiet.views.recipe_editor_view import RecipeEditorView
from codiet.views.recipe_types_editor_view import RecipeTypesEditorView
from codiet.views.meal_goal_editor_view import MealGoalEditorView
from codiet.views.day_plan_editor_view import DayPlanEditorView
from codiet.views.meal_goal_defaults_editor_view import MealGoalDefaultsEditorView

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
        self.recipe_types_editor_view = RecipeTypesEditorView()
        self.meal_goal_editor_view = MealGoalEditorView()
        self.day_plan_editor_view = DayPlanEditorView()
        self.meal_goal_defaults_editor_view = MealGoalDefaultsEditorView()
        # Add the pages to the stacked widget
        self.stacked_widget.addWidget(self.ingredient_editor_view)
        self.stacked_widget.addWidget(self.recipe_editor_view)
        self.stacked_widget.addWidget(self.recipe_types_editor_view)
        self.stacked_widget.addWidget(self.meal_goal_editor_view)
        self.stacked_widget.addWidget(self.day_plan_editor_view)
        self.stacked_widget.addWidget(self.meal_goal_defaults_editor_view)
        # Init the popup windows
        self.ingredient_search_view = IngredientSearchPopupView()

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
        # Create a "Delete Ingredient" action
        self.delete_ingredient_action = QAction("Delete Ingredient", self)
        ingredients_menu.addAction(self.delete_ingredient_action)

        # Create the Recipes menu
        recipes_menu = QMenu("Recipes", self)
        menu_bar.addMenu(recipes_menu)
        # Create the "New Recipe" action
        self.new_recipe_action = QAction("New Recipe", self)
        recipes_menu.addAction(self.new_recipe_action)
        # Create the "Edit Recipe" action
        self.edit_recipe_action = QAction("Edit Recipe", self)
        recipes_menu.addAction(self.edit_recipe_action)
        # Create an "Edit Recipe Types" action
        self.edit_recipe_types_action = QAction("Edit Recipe Types", self)
        recipes_menu.addAction(self.edit_recipe_types_action)
        # Create a "Delete Recipe" action
        self.delete_recipe_action = QAction("Delete Recipe", self)
        recipes_menu.addAction(self.delete_recipe_action)

        # Create the Meal Goals menu
        meal_goals_menu = QMenu("Meal Goals", self)
        menu_bar.addMenu(meal_goals_menu)
        # Create the 'New Meal Goal' action
        self.new_meal_goal_action = QAction("New Meal Goal", self)
        meal_goals_menu.addAction(self.new_meal_goal_action)
        # Create the 'Edit Meal Goal' action
        self.edit_meal_goal_action = QAction("Edit Meal Goal", self)
        meal_goals_menu.addAction(self.edit_meal_goal_action)
        # Create the 'Delete Meal Goal' action
        self.delete_meal_goal_action = QAction("Delete Meal Goal", self)
        meal_goals_menu.addAction(self.delete_meal_goal_action)

        # Create the Day Plans menu
        day_plans_menu = QMenu("Day Plans", self)
        menu_bar.addMenu(day_plans_menu)
        # Create the 'New Day Plan' action
        self.new_day_plan_action = QAction("New Day Plan", self)
        day_plans_menu.addAction(self.new_day_plan_action)
        # Create the 'Edit Day Plan' action
        self.edit_day_plan_action = QAction("Edit Day Plan", self)
        day_plans_menu.addAction(self.edit_day_plan_action)
        # Create the 'Delete Day Plan' action
        self.delete_day_plan_action = QAction("Delete Day Plan", self)
        day_plans_menu.addAction(self.delete_day_plan_action)

        # Create the Run menu
        run_menu = QMenu("Run", self)
        menu_bar.addMenu(run_menu)
        # Add a "Solve Day Plan" action
        self.solve_day_plan_action = QAction("Solve Day Plan", self)
        run_menu.addAction(self.solve_day_plan_action)

        # Create a "Results" menu
        results_menu = QMenu("Results", self)
        menu_bar.addMenu(results_menu)
        # Add a "View Result" action
        self.view_result_action = QAction("View Result", self)
        results_menu.addAction(self.view_result_action)

        # Create the Preferences menu
        preferences_menu = QMenu("Preferences", self)
        menu_bar.addMenu(preferences_menu)
        # Add a set meal goal defaults action
        self.edit_meal_goal_defaults_action = QAction("Edit Meal Goal Defaults", self)
        preferences_menu.addAction(self.edit_meal_goal_defaults_action)

        # Create the Help menu
        help_menu = QMenu("Help", self)
        menu_bar.addMenu(help_menu)

    def show_ingredient_editor(self):
        """Switches the panel to the ingdredient editor."""
        self.stacked_widget.setCurrentIndex(0)

    def show_ingredient_search_popup(self):
        """Opens the ingredient search popup."""
        self.ingredient_search_view.show()

    def show_recipe_editor(self):
        """Switches the panel to the recipe editor."""
        self.stacked_widget.setCurrentIndex(1)

    def show_recipe_types_editor(self):
        """Switches the panel to the recipe types editor."""
        self.stacked_widget.setCurrentIndex(2)

    def show_meal_goal_editor(self):
        """Switches the panel to the meal goal editor."""
        self.stacked_widget.setCurrentIndex(3)

    def show_day_plan_editor(self):
        """Switches the panel to the day plan editor."""
        self.stacked_widget.setCurrentIndex(4)

    def show_meal_goal_defaults_editor(self):
        """Opens the meal goal defaults editor."""
        self.stacked_widget.setCurrentIndex(5)
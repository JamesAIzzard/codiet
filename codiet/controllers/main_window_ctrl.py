from codiet.utils.search import filter_text
from codiet.models.recipes import Recipe
from codiet.db.database_service import DatabaseService
from codiet.views.dialog_box_views import ErrorDialogBoxView
from codiet.views.main_window_view import MainWindowView
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.recipe_editor_view import RecipeEditorView
from codiet.views.meal_planner_view import MealPlannerView
from codiet.controllers.ingredient_editor_ctrl import IngredientEditorCtrl
from codiet.controllers.recipe_editor_ctrl import RecipeEditorCtrl
from codiet.controllers.meal_planner_ctrl import MealPlannerCtrl


class MainWindowCtrl:
    """The main window controller for the CoDiet application."""

    def __init__(self, view: MainWindowView):
        self.view = view  # stash the main window view

        # Add the pages to the view
        self.view.add_page("ingredient-editor", IngredientEditorView())
        self.view.add_page("recipe-editor", RecipeEditorView())
        self.view.add_page("meal-planner", MealPlannerView())

        # Init popup windows
        self.error_popup = ErrorDialogBoxView(parent=self.view)

        # Instantiate the controllers
        self.ingredient_editor_ctrl = IngredientEditorCtrl(self.view._pages["ingredient-editor"])
        self.recipe_editor_ctrl = RecipeEditorCtrl(self.view._pages["recipe-editor"])
        self.meal_planner_ctrl = MealPlannerCtrl(self.view._pages["meal-planner"])

        # Connect up the signals
        self._connect_menu_bar_signals()

        # Cache names for search
        self.ingredient_names = []
        self.recipe_names = []

        # Since the ingredient editor is showing first, 
        # select the ingredient button on the nav bar
        self.view.btn_ingredients.select()

    def _on_ingredients_clicked(self):
        """Handle the user clicking the ingredients button."""
        # Show the editor
        self.view.show_page("ingredient-editor")
        # Deselect the other nav buttons
        self.view.deselect_all_nav_buttons()
        # Highlight the ingredients button
        self.view.btn_ingredients.select()

    def _on_recipes_clicked(self):
        """Handle the user clicking the New Recipe button."""
        # Put a new recipe in the editor
        self.recipe_editor_ctrl.load_recipe_instance(Recipe())
        # Show the editor
        self.view.show_page("recipe-editor")
        # Deselect the other nav buttons
        self.view.deselect_all_nav_buttons()
        # Highlight the recipes button
        self.view.btn_recipes.select()

    def _on_meal_planner_clicked(self):
        """Handle the user clicking the Meal Planner button."""
        self.view.show_page("meal-planner")
        # Deselect the other nav buttons
        self.view.deselect_all_nav_buttons()
        # Highlight the recipes button
        self.view.btn_meal_planner.select()        

    def _connect_menu_bar_signals(self):
        """Connect the signals from the menu bar to the appropriate slots."""
        self.view.ingredientsClicked.connect(self._on_ingredients_clicked)
        self.view.recipesClicked.connect(self._on_recipes_clicked)
        self.view.mealPlannerClicked.connect(self._on_meal_planner_clicked)
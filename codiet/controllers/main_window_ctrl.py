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
        self.ingredient_editor_ctrl = IngredientEditorCtrl(self.view.pages["ingredient-editor"])
        self.recipe_editor_ctrl = RecipeEditorCtrl(self.view.pages["recipe-editor"])
        self.meal_planner_ctrl = MealPlannerCtrl(self.view.pages["meal-planner"])

        # Connect up the signals
        self._connect_menu_bar_signals()

        # Cache names for search
        self.ingredient_names = []
        self.recipe_names = []

        # Since the ingredient editor is showing first, 
        # load an ingredient instance into the editor
        with DatabaseService() as db_service:
            self.ingredient_editor_ctrl.load_ingredient_instance(
                db_service.create_empty_ingredient()
            )

    def _on_new_ingredient_clicked(self):
        """Handle the user clicking the New Ingredient button."""
        # Show the editor
        self.view.show_page("ingredient-editor")

    def _on_delete_ingredient_clicked(self):
        """Handle the user clicking the Delete Ingredient button."""
        # Configure error box to say not implemented
        raise NotImplementedError("Delete Ingredient functionality not yet implemented.")

    def _on_new_recipe_clicked(self):
        """Handle the user clicking the New Recipe button."""
        # Put a new recipe in the editor
        self.recipe_editor_ctrl.load_recipe_instance(Recipe())
        # Show the editor
        self.view.show_page("recipe-editor")

    def _on_meal_planner_clicked(self):
        """Handle the user clicking the Meal Planner button."""
        print("Meal Planner clicked")
        self.view.show_page("meal-planner")

    def _connect_menu_bar_signals(self):
        """Connect the signals from the menu bar to the appropriate slots."""
        self.view.ingredientsClicked.connect(self._on_new_ingredient_clicked)
        self.view.recipesClicked.connect(self._on_new_recipe_clicked)
        self.view.mealPlannerClicked.connect(self._on_meal_planner_clicked)
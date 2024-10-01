
from codiet.sqlite_db.database_service import DatabaseService
from codiet.views.main_window_view import MainWindowView
from codiet.views.ingredients.ingredient_editor_view import IngredientEditorView
from codiet.views.recipe_editor_view import RecipeEditorView
from codiet.views.meal_planner_view import MealPlannerView
from codiet.controllers import BaseController
from codiet.controllers.ingredient_editor import IngredientEditor
from codiet.controllers.recipe_editor_ctrl import RecipeEditor
from codiet.controllers.meal_planner import MealPlanner


class MainWindow(BaseController[MainWindowView]):
    """The main window controller for the CoDiet application."""

    def __init__(self, db_service: DatabaseService, *args, **kwargs):
        """Initialise the main window controller.

        Args:
            db_service (DatabaseService): The database service.
        """
        super().__init__(*args, **kwargs)

        # Stash the database service instance
        self.db_service = db_service

        # Instantiate the page modules
        self.ingredient_editor = IngredientEditor(parent=self.view, db_service=self.db_service)
        # self.recipe_editor = RecipeEditor(parent=self.view, db_service=self.db_service)
        # self.meal_planner = MealPlanner(parent=self.view, db_service=self.db_service)

        # Add the pages to the view
        self.view.add_page("ingredient-editor", self.ingredient_editor.view)
        # self.view.add_page("recipe-editor", self.recipe_editor.view)
        # self.view.add_page("meal-planner", self.meal_planner.view)

        # Connect up the signals
        self._connect_menu_bar_signals()

        # Since the ingredient editor is showing first, 
        # select the ingredient button on the nav bar
        self.view.btn_ingredients.select()

    def show(self):
        """Show the main window."""
        self.view.show()

    def _create_view(self, *args, **kwargs) -> MainWindowView:
        return MainWindowView(*args, **kwargs)

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
        # self.recipe_editor_ctrl.load_recipe_instance(Recipe())
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
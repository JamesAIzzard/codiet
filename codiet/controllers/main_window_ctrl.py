from codiet.db.database_service import DatabaseService
from codiet.views.main_window_view import MainWindowView
from codiet.controllers.ingredient_editor_ctrl import IngredientEditorCtrl
from codiet.controllers.ingredient_search_popup_ctrl import IngredientSearchPopupCtrl
from codiet.controllers.recipe_editor_ctrl import RecipeEditorCtrl

class MainWindowCtrl:
    def __init__(self, view:MainWindowView, db_service:DatabaseService):
        self.view = view
        self.db_service = db_service

        # Instantiate the ingredient editor controller
        self.ingredient_editor_ctrl = IngredientEditorCtrl(
            self.view.ingredient_editor_view, self.db_service
        )
        # Instantiate the ingredient search popup controller
        self.ingredient_search_popup_ctrl = IngredientSearchPopupCtrl(
            self.view.ingredient_search_view, self.db_service
        )
        # Instantiate the recipe editor controller
        self.recipe_editor_ctrl = RecipeEditorCtrl(
            self.view.recipe_editor_view, self.db_service
        )

        # Connect the signals and slots
        self.view.new_ingredient_action.triggered.connect(self.on_new_ingredient_clicked)
        self.view.edit_ingredient_action.triggered.connect(self.on_edit_ingredient_clicked)
        self.view.new_recipe_action.triggered.connect(self.on_new_recipe_clicked)
        self.view.edit_recipe_types_action.triggered.connect(self.on_edit_recipe_types_clicked)
        self.view.new_meal_goal_action.triggered.connect(self.on_new_meal_goal_clicked)
        self.view.new_day_plan_action.triggered.connect(self.on_new_day_plan_clicked)
        self.view.edit_meal_goal_defaults_action.triggered.connect(self.on_meal_goal_defaults_clicked)

    def on_new_ingredient_clicked(self):
        """Handle the user clicking the New Ingredient button."""
        self.view.show_ingredient_editor()
        print("New Ingredient clicked")

    def on_edit_ingredient_clicked(self):
        """Handle the user clicking the Edit Ingredient button."""
        self.view.show_ingredient_search_popup()
        print("Edit Ingredient clicked")

    def on_new_recipe_clicked(self):
        """Handle the user clicking the New Recipe button."""
        self.view.show_recipe_editor()

    def on_edit_recipe_types_clicked(self):
        """Handle the user clicking the Edit Recipe Types button."""
        self.view.show_recipe_types_editor()

    def on_new_meal_goal_clicked(self):
        """Handle the user clicking the New Meal Goal button."""
        self.view.show_meal_goal_editor()

    def on_new_day_plan_clicked(self):
        """Handle the user clicking the New Day Plan button."""
        self.view.show_day_plan_editor()

    def on_meal_goal_defaults_clicked(self):
        """Handle the user clicking the Meal Goal Defaults button."""
        self.view.show_meal_goal_defaults_editor()
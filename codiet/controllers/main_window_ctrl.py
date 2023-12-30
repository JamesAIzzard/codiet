from codiet.db.database_service import DatabaseService
from codiet.views.main_window_view import MainWindowView
from codiet.controllers.ingredient_editor_ctrl import IngredientEditorCtrl

class MainWindowCtrl:
    def __init__(self, view:MainWindowView, db_service:DatabaseService):
        self.view = view
        self.db_service = db_service

        # Instantiate the ingredient editor controller
        self.ingredient_editor_ctrl = IngredientEditorCtrl(
            self.view.ingredient_editor_view, self.db_service
        )

        # Connect the signals and slots
        self.view.new_ingredient_action.triggered.connect(self.on_new_ingredient_clicked)
        self.view.new_recipe_action.triggered.connect(self.on_new_recipe_clicked)
        self.view.new_meal_goal_action.triggered.connect(self.on_new_meal_goal_clicked)

    def on_new_ingredient_clicked(self):
        self.view.show_ingredient_editor()
        print("New Ingredient clicked")

    def on_new_recipe_clicked(self):
        self.view.show_recipe_editor()
        print("New Recipe clicked")

    def on_new_meal_goal_clicked(self):
        self.view.show_meal_goal_editor()
        print("New Meal Goal clicked")
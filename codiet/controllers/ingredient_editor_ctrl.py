from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.flag_editor_view import FlagEditorView
from codiet.controllers.flag_editor_ctrl import FlagEditorCtrl
from codiet.controllers.ingredient_nutrients_editor_ctrl import IngredientNutrientsEditorCtrl

class IngredientEditorCtrl:
    def __init__(self, view: IngredientEditorView, db_service:DatabaseService):
        self.view = view
        self.db_service = db_service

        # Instantiate the ingredient flag editor controller
        self.ingredient_flag_editor_ctrl = FlagEditorCtrl(
            self.view.flag_editor_view, self.db_service
        )

        # Instantiate the ingredient nutrient editor controller
        self.ingredient_nutrients_editor_ctrl = IngredientNutrientsEditorCtrl(
            self.view.nutrient_editor_view, self.db_service
        )
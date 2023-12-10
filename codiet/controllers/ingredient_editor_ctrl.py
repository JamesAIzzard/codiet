from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.ingredient_flag_editor_view import IngredientFlagEditorView
from codiet.controllers.ingredient_flag_editor_ctrl import IngredientFlagEditorCtrl

class IngredientEditorCtrl:
    def __init__(self, view: IngredientEditorView, db_service:DatabaseService):
        self.view = view
        self.db_service = db_service

        # Instantiate the ingredient flag editor controller
        self.ingredient_flag_editor_ctrl = IngredientFlagEditorCtrl(
            self.view.flag_editor_view, self.db_service
        )
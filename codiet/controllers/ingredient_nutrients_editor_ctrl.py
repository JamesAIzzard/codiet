from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_nutrients_editor_view import IngredientNutrientsEditorView

class IngredientNutrientsEditorCtrl:
    def __init__(self, view: IngredientNutrientsEditorView, db_service: DatabaseService):
        self.view = view
        self.db_service = db_service
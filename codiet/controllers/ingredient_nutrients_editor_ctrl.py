from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_nutrients_editor_view import IngredientNutrientsEditorView

class IngredientNutrientsEditorCtrl:
    def __init__(self, view: IngredientNutrientsEditorView, db_service: DatabaseService):
        self.view = view
        self.db_service = db_service

        # Populate the list of mandatory nutrients
        # First grab the mandatory nutrients from the DB
        mandatory_nutrient_names = self.db_service.get_mandatory_nutrient_names()
        # Then add them to the list
        for nutrient in mandatory_nutrient_names:
            self.view.add_nutrient(nutrient)
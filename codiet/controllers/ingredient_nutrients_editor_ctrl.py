from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_nutrients_editor_view import IngredientNutrientsEditorView

class IngredientNutrientsEditorCtrl:
    """Controller for the IngredientNutrientsEditorView."""
    def __init__(self, view: IngredientNutrientsEditorView, db_service: DatabaseService):
        self.view = view
        self.db_service = db_service

        # Populate the nutrient list
        self.load_ingredient_nutrients()

    def load_ingredient_nutrients(self) -> None:
        """Pulls all nutrients from the DB and loads them into the UI list."""
        nutrients = self.db_service.get_all_nutrient_names()
        for nutrient in nutrients:
            self.view.add_nutrient(nutrient)
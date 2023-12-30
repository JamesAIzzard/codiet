from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_search_popup_view import IngredientSearchPopupView

class IngredientSearchPopupCtrl:
    def __init__(self, view:IngredientSearchPopupView, db_service:DatabaseService):
        self.view = view
        self.db_service = db_service

        # When a key is pressed in the search box, update the list of matching ingredients
        self.view.txt_search.textChanged.connect(self.on_search_box_text_changed)

    def on_search_box_text_changed(self, text):
        """Handle the user typing in the search box."""
        # Get the list of matching ingredient names
        matching_names = self.db_service.load_matching_ingredient_names(text)
        # Update the list of matching ingredients
        self.view.update_ingredient_list(matching_names)


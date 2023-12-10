from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_flag_editor_view import IngredientFlagEditorView


class IngredientFlagEditorCtrl:
    def __init__(self, view: IngredientFlagEditorView, db_service: DatabaseService):
        self.view = view
        self.db_service = db_service

        # Grab a list of all flags
        self.flags = self.db_service.get_all_flags()
        # Work through each flag and populate the list
        for flag in self.flags:
            # Capitalise each word in the flag name
            flag = flag.title()
            self.view.add_flag_to_list(flag)
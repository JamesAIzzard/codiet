from codiet.views.recipe_editor_view import RecipeEditorView
from codiet.controllers.serve_time_intervals_editor_ctrl import ServeTimeIntervalsEditorCtrl
from codiet.db.database_service import DatabaseService

class RecipeEditorCtrl:
    def __init__(self, view: RecipeEditorView):
        self.view = view

        # Instantiate the time interval editor controller
        self.time_intervals_editor_ctrl = ServeTimeIntervalsEditorCtrl(
            self.view.serve_time_intervals_editor_view
        )
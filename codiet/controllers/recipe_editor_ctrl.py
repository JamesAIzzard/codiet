from codiet.models.recipe import Recipe
from codiet.views.recipe_editor_view import RecipeEditorView
from codiet.controllers.serve_time_intervals_editor_ctrl import ServeTimeIntervalsEditorCtrl
from codiet.db.database_service import DatabaseService

class RecipeEditorCtrl:
    def __init__(self, view: RecipeEditorView):

        # Stash a reference to the view
        self.view = view

        # Store the state of the editor
        self.edit_mode = False

        # Instantiate the time interval editor controller
        self.time_intervals_editor_ctrl = ServeTimeIntervalsEditorCtrl(
            self.view.serve_time_intervals_editor_view
        )

    def load_recipe_instance(self, recipe:Recipe) -> None:
        """Load a recipe instance into the editor."""
        # Update the stored instance
        self.recipe = recipe
        # Update the recipe name field
        self.view.update_name(recipe.name)
        # Update the recipe description field
        self.view.update_description(recipe.description)
        # Update the instructions field
        self.view.update_instructions(recipe.instructions)
        # Update the ingredients fields
        self.view.update_ingredients(recipe.ingredients)
        # Update the time intervals field
        self.view.serve_time_intervals_editor_view.update_serve_times(recipe.serve_times)
        # Update the recipe type field 
        self.view.update_recipe_types(recipe.recipe_types)
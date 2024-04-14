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
        # Connect the signals and slots
        self._connect_signals_and_slots()

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

    def on_recipe_name_changed(self, name: str) -> None:
        """Handle the recipe name being changed."""
        # If the name is empty, set it to None
        if name.strip() == "":
            self.recipe.name = None
        # Otherwise, set the name
        else:
            self.recipe.name = name

    def on_recipe_description_changed(self) -> None:
        """Handle the recipe description being changed."""
        description = self.view.txt_recipe_description.toPlainText()
        # If the description is empty, set it to None
        if description.strip() == "":
            self.recipe.description = None
        # Otherwise, set the description
        else:
            self.recipe.description = description

    def on_recipe_instructions_changed(self) -> None:
        """Handle the recipe instructions being changed."""
        instructions = self.view.textbox_recipe_instructions.toPlainText()
        # If the instructions are empty, set them to None
        if instructions.strip() == "":
            self.recipe.instructions = None
        # Otherwise, set the instructions
        else:
            self.recipe.instructions = instructions

    def on_save_button_pressed(self) -> None:
        """Handle the save button being pressed."""
        # If we are saving a new recipe
        if self.recipe.id is None:
            # Save it
            with DatabaseService() as db_service:
                self.recipe.id = self.recipe.id = db_service.insert_new_recipe(self.recipe)
            # Open a popup to confirm the save
            self.view.show_save_confirmation_popup()
        # Otherwise, update the existing recipe
        else:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
            # Open a popup to confirm the update
            self.view.show_update_confirmation_popup()

    def _connect_signals_and_slots(self) -> None:
        """Connect the signals and slots for the recipe editor."""
        # Connect the recipe name changed signal
        self.view.txt_recipe_name.textChanged.connect(self.on_recipe_name_changed)
        # Connect the recipe description changed signal
        self.view.txt_recipe_description.textChanged.connect(self.on_recipe_description_changed)
        # Connect the recipe instructions changed signal
        self.view.textbox_recipe_instructions.textChanged.connect(self.on_recipe_instructions_changed)
        # Connect the save button
        self.view.btn_save_recipe.clicked.connect(self.on_save_button_pressed)

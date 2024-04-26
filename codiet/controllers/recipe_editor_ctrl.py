from datetime import datetime

from codiet.utils.search import filter_text
from codiet.models.recipe import Recipe
from codiet.views.recipe_editor_view import RecipeEditorView
from codiet.controllers.serve_time_intervals_editor_ctrl import ServeTimeIntervalsEditorCtrl
from codiet.views.recipe_type_selector_popup_view import RecipeTypeSelectorPopupView
from codiet.controllers.ingredients_editor_ctrl import IngredientsEditorCtrl
from codiet.db.database_service import DatabaseService

class RecipeEditorCtrl:
    def __init__(self, view: RecipeEditorView):
        # Stash a reference to the view
        self.view = view
        # Init a recipe instance
        with DatabaseService() as db_service:
            self.recipe = db_service.create_empty_recipe()
        # Instantiate the ingredients editor controller
        self.ingredients_editor_ctrl = IngredientsEditorCtrl(
            view = self.view.ingredients_editor,
            recipe = self.recipe
        )
        # Instantiate the time interval editor controller
        self.time_intervals_editor_ctrl = ServeTimeIntervalsEditorCtrl(
            view = self.view.serve_time_intervals_editor_view,
            on_add_time_interval=self._on_add_serve_time,
            on_remove_time_interval=self._on_remove_serve_time
        )
        # Build the recipe type selector popup
        self._setup_recipe_type_views()
        # Connect the signals and slots
        # TODO: Update this to use better organised setup methods as
        # done with the recipe types stuff.
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
        self.view.serve_time_intervals_editor_view.update_serve_times(recipe.serve_times_strings)
        # Update the recipe type field 
        self.view.update_recipe_types(recipe.recipe_types)

    def _on_recipe_name_changed(self, name: str) -> None:
        """Handle the recipe name being changed."""
        # If the name is empty, set it to None
        if name.strip() == "":
            self.recipe.name = None
        # Otherwise, set the name
        else:
            self.recipe.name = name

    def _on_recipe_description_changed(self) -> None:
        """Handle the recipe description being changed."""
        description = self.view.txt_recipe_description.toPlainText()
        # If the description is empty, set it to None
        if description.strip() == "":
            self.recipe.description = None
        # Otherwise, set the description
        else:
            self.recipe.description = description

    def _on_recipe_instructions_changed(self) -> None:
        """Handle the recipe instructions being changed."""
        instructions = self.view.textbox_recipe_instructions.toPlainText()
        # If the instructions are empty, set them to None
        if instructions.strip() == "":
            self.recipe.instructions = None
        # Otherwise, set the instructions
        else:
            self.recipe.instructions = instructions

    def _on_add_serve_time(self, serve_time: tuple[datetime, datetime]) -> None:
        """Handle the addition of a serve time."""
        self.recipe.add_serve_time(serve_time)

    def _on_remove_serve_time(self, serve_time: tuple[datetime, datetime]) -> None:
        """Handle the removal of a serve time."""
        self.recipe.remove_serve_time(serve_time)

    def _on_add_recipe_type_clicked(self) -> None:
        """Handle the add recipe type button being clicked."""
        # Rebuild the cached recipe types
        with DatabaseService() as db_service:
            self.recipe_types = db_service.fetch_all_global_recipe_types()
        # Add all of these types to the popup
        self.recipe_type_selector_popup.update_recipe_types(self.recipe_types)
        # Show the popup
        self.recipe_type_selector_popup.show()

    def _on_recipe_type_selected(self, recipe_type: str) -> None:
        """Handle a recipe type being selected."""
        # Add the type to the view
        self.view.recipe_type_editor_view.add_recipe_type(recipe_type)
        # Add the type to the recipe
        self.recipe.add_recipe_type(recipe_type)

    def _on_remove_recipe_type_clicked(self) -> None:
        """Handle the remove recipe type button being clicked."""
        # Get the selected recipe type
        recipe_type = self.view.recipe_type_editor_view.selected_recipe_type
        # If there is no selected recipe type, return
        if recipe_type is None:
            return None
        # Remove the recipe type from the view
        self.view.recipe_type_editor_view.remove_recipe_type(recipe_type)
        # Remove the recipe type from the recipe
        self.recipe.remove_recipe_type(recipe_type)

    def _on_recipe_type_search_term_changed(self, search_term: str) -> None:
        """Handle the search term being changed."""
        # If the search term is empty, return
        if search_term.strip() == "":
            # Update the recipe types in the popup
            self.recipe_type_selector_popup.update_recipe_types(self.recipe_types)
        # Otherwise, find the best matching recipe types
        else:
            # Filter the recipe types
            filtered_recipe_types = filter_text(search_term, self.recipe_types, 2)
            # Update the recipe types in the popup
            self.recipe_type_selector_popup.update_recipe_types(filtered_recipe_types)

    def _setup_recipe_type_views(self) -> None:
        """Initialize the recipe type selector popup."""
        # Connect the add recipe type button to the recipe type popup
        self.view.recipe_type_editor_view.addRecipeTypeClicked.connect(self._on_add_recipe_type_clicked)
        # Connect the remove recipe type button to the recipe type popup
        self.view.recipe_type_editor_view.removeRecipeTypeClicked.connect(self._on_remove_recipe_type_clicked)
        # Init the popup
        self.recipe_type_selector_popup = RecipeTypeSelectorPopupView()
        # Connect the recipe type selected signal
        self.recipe_type_selector_popup.recipeTypeSelected.connect(self._on_recipe_type_selected)
        # Connect the search term changed signal
        self.recipe_type_selector_popup.searchTermChanged.connect(self._on_recipe_type_search_term_changed)

    def _on_save_button_pressed(self) -> None:
        """Handle the save button being pressed."""
        # Open the 'name required' popup if the name is empty
        if self.recipe.name is None or self.recipe.name.strip() == "":
            self.view.show_name_required_popup()
            return None
        # If we are saving a new recipe (there is no ID yet)
        if self.recipe.id is None:
            # Save it
            with DatabaseService() as db_service:
                self.recipe.id = self.recipe.id = db_service.insert_new_recipe(self.recipe)
            # Open a popup to confirm the save
            self.view.show_save_confirmation_popup()
            return None
        # So the id is populated, this must be an update.
        # First fetch the name from the database which corresponds to this id.
        with DatabaseService() as db_service:
            existing_name = db_service.fetch_recipe_name(self.recipe.id)
        # If the name has changed
        if existing_name != self.recipe.name:
            # Open a yes/no popup to confirm the update
            response = self.view.show_name_change_confirmation_popup()
            # If the user clicked no, return
            if response == False:
                return None
        # If the name has not changed, go ahead and update
        with DatabaseService() as db_service:
            db_service.update_recipe(self.recipe)
        # Open a popup to confirm the update
        self.view.show_update_confirmation_popup()

    def _connect_signals_and_slots(self) -> None:
        """Connect the signals and slots for the recipe editor."""
        # Connect the recipe name changed signal
        self.view.txt_recipe_name.textChanged.connect(self._on_recipe_name_changed)
        # Connect the recipe description changed signal
        self.view.txt_recipe_description.textChanged.connect(self._on_recipe_description_changed)
        # Connect the recipe instructions changed signal
        self.view.textbox_recipe_instructions.textChanged.connect(self._on_recipe_instructions_changed)
        # Connect the save button
        self.view.btn_save_recipe.clicked.connect(self._on_save_button_pressed)

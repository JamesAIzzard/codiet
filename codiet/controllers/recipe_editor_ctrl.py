from datetime import datetime

from codiet.utils.search import filter_text
from codiet.utils.time import (
    convert_datetime_interval_to_time_string_interval,
    convert_time_string_interval_to_datetime_interval,
)
from codiet.utils.recipes import convert_recipe_to_json, save_recipe_datafile
from codiet.models.recipes import Recipe
from codiet.models.ingredients import IngredientQuantity
from codiet.views.recipe_editor_view import RecipeEditorView
from codiet.views.dialog_box_views import ErrorDialogBoxView
from codiet.views.time_interval_popup_view import TimeIntervalPopupView
from codiet.db.database_service import DatabaseService


class RecipeEditorCtrl:
    def __init__(self, view: RecipeEditorView):
        # Stash a reference to the view
        self.view = view

        # Init ancillairy views
        self.serve_time_popup = TimeIntervalPopupView()
        self.error_popup = ErrorDialogBoxView(message="", title="", parent=self.view)
        self.name_required_popup = ErrorDialogBoxView(
            message="Please provide a name for the recipe.",
            title="Name Required",
            parent=self.view,
        )

        # Cache some searchable things
        self.all_ingredient_names: list[str] = []
        self.recipe_types: list[str] = []

        # Connect the ingredient editor views
        self._connect_ingredients_editor()
        self._connect_serve_time_editor()
        self._connect_recipe_type_editor()
        self._connect_basic_info_fields()
        self._connect_save_buttons()

    def load_recipe_instance(self, recipe: Recipe) -> None:
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
        for ingredient_quantity in recipe.ingredient_quantities.values():
            # If the ingredient name or ID are None, raise exception
            if (
                ingredient_quantity.ingredient.name is None
                or ingredient_quantity.ingredient.id is None
            ):
                raise ValueError("Ingredient name or ID is None.")
            # Add the widget to the view
            self.view.ingredients_editor.add_ingredient_quantity(
                ingredient_name=ingredient_quantity.ingredient.name,
                ingredient_id=ingredient_quantity.ingredient.id,
                ingredient_quantity_value=ingredient_quantity.qty_value,
                ingredient_quantity_unit=ingredient_quantity.qty_unit,
                ingredient_quantity_upper_tol=ingredient_quantity.upper_tol,
                ingredient_quantity_lower_tol=ingredient_quantity.lower_tol,
            )
        # Update the time intervals field
        for interval in recipe.serve_times:
            self.view.serve_time_intervals_editor_view.add_time_interval(
                convert_datetime_interval_to_time_string_interval(interval)
            )
        # Update the recipe type field
        self.view.update_recipe_types(recipe._recipe_types)

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

    # def _on_add_ingredient_clicked(self) -> None:
    #     """Handle the add ingredient button being clicked."""
    #     # Cache the current list of ingredient names
    #     with DatabaseService() as db_service:
    #         self.all_ingredient_names = db_service.fetch_all_ingredient_names()
    #     # Show the ingredient search popup
    #     self.ingredients_editor_popup.show()

    def _on_remove_ingredient_clicked(self) -> None:
        """Handle the remove ingredient button being clicked."""
        # Get the selected ingredient id
        ingredient_id = self.view.ingredients_editor.selected_ingredient_id
        # If there is no selected ingredient, return
        if ingredient_id is None:
            return None
        # Remove the ingredient from the recipe
        self.recipe.remove_ingredient_quantity(ingredient_id)
        # Update the ingredients in the view
        self.view.ingredients_editor.remove_ingredient_quantity(ingredient_id)

    # def _on_ingredient_search_term_changed(self, search_term: str) -> None:
    #     """Handle the ingredient search term being changed."""
    #     # If the search term is empty, return
    #     if search_term.strip() == "":
    #         return None
    #     # Filter the ingredients
    #     filtered_ingredient_names = filter_text(
    #         search_term, self.all_ingredient_names, 5
    #     )
    #     # Update the ingredients in the popup
    #     self.ingredients_editor_popup.update_results_list(filtered_ingredient_names)

    # def _on_ingredient_search_cancelled(self) -> None:
    #     """Handle the ingredient search being cancelled."""
    #     # Clear the contents of the search term textbox
    #     self.ingredients_editor_popup.search_term_textbox.clear()

    # def _on_ingredient_selected(self, ingredient_name: str) -> None:
    #     """Handle an ingredient being selected."""
    #     # Fetch the ingredient data from the database
    #     with DatabaseService() as db_service:
    #         ingredient = db_service.fetch_ingredient_by_name(ingredient_name)
    #     # Create a new recipe ingredient instance
    #     ingredient_qty = IngredientQuantity(ingredient)
    #     # Add the ingredient to the recipe
    #     self.recipe.add_ingredient_quantity(ingredient_quantity=ingredient_qty)
    #     # Assert the ingredient id is set
    #     assert ingredient.id is not None
    #     # Add the ingredient to the view
    #     self.view.ingredients_editor.add_ingredient_quantity(
    #         ingredient_name=ingredient_name, ingredient_id=ingredient.id
    #     )
    #     # Hide the popup
    #     self.ingredients_editor_popup.hide()

    def _on_ingredient_qty_changed(self, ingredient_id: int, qty: float) -> None:
        """Handle the ingredient quantity being changed."""
        # Update the ingredient quantity in the recipe
        self.recipe.update_ingredient_quantity_value(ingredient_id, qty)

    def _on_ingredient_qty_unit_changed(self, ingredient_id: int, unit: str) -> None:
        """Handle the ingredient quantity unit being changed."""
        # Update the ingredient quantity unit in the recipe
        self.recipe.update_ingredient_quantity_unit(ingredient_id, unit)

    def _on_ingredient_qty_utol_changed(self, ingredient_id: int, utol: float) -> None:
        """Handle the ingredient quantity upper tolerance being changed."""
        # Update the ingredient quantity upper tolerance in the recipe
        self.recipe.update_ingredient_quantity_utol(ingredient_id, utol)

    def _on_ingredient_qty_ltol_changed(self, ingredient_id: int, ltol: float) -> None:
        """Handle the ingredient quantity lower tolerance being changed."""
        # Update the ingredient quantity lower tolerance in the recipe
        self.recipe.update_ingredient_quantity_ltol(ingredient_id, ltol)

    def _on_add_serve_time_clicked(self) -> None:
        """Handle the addition of a serve time."""
        # Show the popup
        self.serve_time_popup.show()

    def _on_remove_serve_time_clicked(self) -> None:
        """Handle the removal of a serve time."""
        # Get the selected index
        index = self.view.serve_time_intervals_editor_view.selected_index
        # If there is no selected index, return
        if index is None:
            return None
        # Create the datetime objects for the start and end times
        datetime_interval = convert_time_string_interval_to_datetime_interval(
            self.view.serve_time_intervals_editor_view.selected_time_interval_string  # type: ignore
        )
        # Remove the time interval from the recipe
        self.recipe.remove_serve_time(datetime_interval)
        # Update the serve times in the view
        self.view.serve_time_intervals_editor_view.remove_time_interval(index)

    def _on_serve_time_provided(self, start_time: str, end_time: str) -> None:
        """Handle a serve time being provided."""
        # Validate the strings as times
        try:
            # Convert the strings to datetime objects
            dt_start = datetime.strptime(start_time, "%H:%M")
            dt_end = datetime.strptime(end_time, "%H:%M")
        except ValueError:
            # Configure the error popup
            self.error_popup.setWindowTitle("Invalid Time")
            self.error_popup.message = "Please enter a valid time."
            # Show the error popup
            self.error_popup.show()
            return None
        # Add the time interval to the recipe
        self.recipe.add_serve_time((dt_start, dt_end))
        # Update the serve times in the view
        self.view.serve_time_intervals_editor_view.add_time_interval(
            convert_datetime_interval_to_time_string_interval((dt_start, dt_end))
        )
        # Hide the popup
        self.serve_time_popup.hide()

    # def _on_add_recipe_type_clicked(self) -> None:
    #     """Handle the add recipe type button being clicked."""
    #     # Rebuild the cached recipe types
    #     with DatabaseService() as db_service:
    #         self.recipe_types = db_service.fetch_all_global_recipe_types()
    #     # Add all of these types to the popup
    #     self.recipe_type_selector_popup.update_results_list(self.recipe_types)
    #     # Show the popup
    #     self.recipe_type_selector_popup.show()

    def _on_recipe_type_selected(self, recipe_type: str) -> None:
        """Handle a recipe type being selected."""
        # If the type is already on the recipe, return
        if recipe_type in self.recipe.recipe_types:
            return None
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

    # def _on_recipe_type_search_term_changed(self, search_term: str) -> None:
    #     """Handle the search term being changed."""
    #     # If the search term is empty, return
    #     if search_term.strip() == "":
    #         # Update the recipe types in the popup
    #         self.recipe_type_selector_popup.update_results_list(self.recipe_types)
    #     # Otherwise, find the best matching recipe types
    #     else:
    #         # Filter the recipe types
    #         filtered_recipe_types = filter_text(search_term, self.recipe_types, 2)
    #         # Update the recipe types in the popup
    #         self.recipe_type_selector_popup.update_results_list(filtered_recipe_types)

    # def _on_clear_recipe_type_search_clicked(self) -> None:
    #     """Handle the clear recipe type search button being clicked."""
    #     # Clear the search term and results list
    #     self.recipe_type_selector_popup.clear_results_list()
    #     self.recipe_type_selector_popup.clear_search_term()
    #     # Repopulate the list with all types
    #     self.recipe_type_selector_popup.update_results_list(self.recipe_types)

    def _on_save_button_clicked(self) -> None:
        """Handle the save button being pressed."""
        # Open the 'name required' popup if the name is empty
        if self.recipe.name is None or self.recipe.name.strip() == "":
            self.name_required_popup.show()
            return None
        # If we are saving a new recipe (there is no ID yet)
        if self.recipe.id is None:
            # Save it
            with DatabaseService() as db_service:
                self.recipe.id = self.recipe.id = db_service.insert_new_recipe(
                    self.recipe
                )
            # Open a popup to confirm the save
            self.view.show_save_confirmation_popup()
            return None
        # So the id is populated, this must be an update.
        # First fetch the name from the database which corresponds to this id.
        with DatabaseService() as db_service:
            existing_name = db_service.fetch_recipe_name_using_id(self.recipe.id)
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

    def _on_save_to_json_button_clicked(self) -> None:
        """Handle the save to JSON button being clicked."""
        # Open the name required popup if the name is empty
        if self.recipe.name is None or self.recipe.name.strip() == "":
            self.name_required_popup.show()
            return None
        # Create a .json datafile representing the recipe
        recipe_data = convert_recipe_to_json(self.recipe)
        try:
            # Save the recipe to the file
            save_recipe_datafile(recipe_data)
        except FileExistsError as e:
            # The file already exists - configure the error popup
            self.error_popup.setWindowTitle("File Exists")
            self.error_popup.message = str(e)
            # Show the error popup
            self.error_popup.show()
            return None
        except ValueError as e:
            # Some other error occurred - configure the error popup
            self.error_popup.setWindowTitle("Error")
            self.error_popup.message = str(e)
            # Show the error popup
            self.error_popup.show()
        # Open a popup to confirm the save
        self.view.show_save_confirmation_popup()


    def _connect_ingredients_editor(self) -> None:
        """Initialise the ingredients editor views."""
        # self.view.ingredients_editor.addIngredientClicked.connect(
        #     self._on_add_ingredient_clicked
        # )
        self.view.ingredients_editor.removeIngredientClicked.connect(
            self._on_remove_ingredient_clicked
        )
        # self.ingredients_editor_popup.search_term_textbox.searchTermChanged.connect(
        #     self._on_ingredient_search_term_changed
        # )
        # self.ingredients_editor_popup.search_term_textbox.cancelClicked.connect(
        #     self._on_ingredient_search_cancelled
        # )
        # self.ingredients_editor_popup.resultSelected.connect(
        #     self._on_ingredient_selected
        # )
        self.view.ingredients_editor.ingredientQtyChanged.connect(
            self._on_ingredient_qty_changed
        )
        self.view.ingredients_editor.ingredientQtyUnitChanged.connect(
            self._on_ingredient_qty_unit_changed
        )
        self.view.ingredients_editor.ingredientQtyUTolChanged.connect(
            self._on_ingredient_qty_utol_changed
        )
        self.view.ingredients_editor.ingredientQtyLTolChanged.connect(
            self._on_ingredient_qty_ltol_changed
        )

    def _connect_serve_time_editor(self) -> None:
        """Initialise the serve time editor views."""
        self.view.serve_time_intervals_editor_view.addServeTimeClicked.connect(
            self._on_add_serve_time_clicked
        )
        self.view.serve_time_intervals_editor_view.removeServeTimeClicked.connect(
            self._on_remove_serve_time_clicked
        )
        self.serve_time_popup.addIntervalClicked.connect(self._on_serve_time_provided)

    def _connect_recipe_type_editor(self) -> None:
        """Initialise the recipe type selector popup."""
        # self.view.recipe_type_editor_view.addRecipeTypeClicked.connect(
        #     self._on_add_recipe_type_clicked
        # )
        # self.view.recipe_type_editor_view.removeRecipeTypeClicked.connect(
        #     self._on_remove_recipe_type_clicked
        # )
        # self.recipe_type_selector_popup.resultSelected.connect(
        #     self._on_recipe_type_selected
        # )
        # self.recipe_type_selector_popup.searchTermCleared.connect(
        #     self._on_clear_recipe_type_search_clicked
        # )
        # self.recipe_type_selector_popup.searchTermChanged.connect(
        #     self._on_recipe_type_search_term_changed
        # )

    def _connect_basic_info_fields(self) -> None:
        """Connect the signals and slots for the recipe editor."""
        # Connect the recipe name changed signal
        self.view.txt_recipe_name.textChanged.connect(self._on_recipe_name_changed)
        # Connect the recipe description changed signal
        self.view.txt_recipe_description.textChanged.connect(
            self._on_recipe_description_changed
        )
        # Connect the recipe instructions changed signal
        self.view.textbox_recipe_instructions.textChanged.connect(
            self._on_recipe_instructions_changed
        )

    def _connect_save_buttons(self) -> None:
        """Connect the save buttons."""
        self.view.saveRecipeClicked.connect(self._on_save_button_clicked)
        self.view.saveToJSONClicked.connect(self._on_save_to_json_button_clicked)

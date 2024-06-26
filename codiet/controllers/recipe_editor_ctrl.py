from datetime import datetime

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QListWidgetItem,
)

from codiet.db.database_service import DatabaseService
from codiet.utils.time import (
    convert_datetime_interval_to_time_string_interval,
    convert_time_string_interval_to_datetime_interval,
)
from codiet.utils.strings import convert_to_snake_case
from codiet.utils.recipes import convert_recipe_to_json, save_recipe_datafile, recipe_datafile_exists
from codiet.models.recipes import Recipe
from codiet.models.ingredients import IngredientQuantity
from codiet.views.dialog_box_views import (
    DialogBoxView,
    EntityNameDialogView, 
    OkDialogBoxView, 
    ConfirmDialogBoxView,
)
from codiet.views.recipe_editor_view import RecipeEditorView
from codiet.views.search import SearchColumnView
from codiet.views.dialog_box_views import ErrorDialogBoxView
from codiet.views.time_interval_popup_view import TimeIntervalPopupView
from codiet.views.tags import RecipeTagSelectorPopup
from codiet.controllers.search import SearchColumnCtrl
from codiet.controllers.entity_name_dialog_ctrl import EntityNameDialogCtrl
from codiet.controllers.tags import RecipeTagEditorCtrl


class RecipeEditorCtrl:
    def __init__(self, view: RecipeEditorView):
        self.view = view
        self.recipe = Recipe()

        # Cache some searchable things
        self._recipe_names: list[str] = []
        self._all_ingredient_names: list[str] = []
        self._recipe_types: list[str] = []
        # Run the caching functions for the first time
        self._cache_recipe_names()
        self._cache_ingredient_names()

        # Configure name editor
        self.recipe_name_editor_view = EntityNameDialogView(
            entity_name="Recipe",
            parent=self.view
        )
        self.recipe_name_editor_ctrl = EntityNameDialogCtrl(
            view=self.recipe_name_editor_view,
            check_name_available=lambda name: name not in self._recipe_names,
            on_name_accepted=self._on_recipe_name_accepted,
        )  

        # Configure search column controller
        self.search_column_ctrl = SearchColumnCtrl(
            view=self.view.recipe_search,
            get_searchable_strings=lambda: self._recipe_names,
            on_result_selected=self._on_recipe_selected,
        )   

        # Configure the ingredient search popup
        # First init a search column
        self.ingredient_search_column_view = SearchColumnView()
        self.ingredient_search_column_ctrl = SearchColumnCtrl(
            view=self.ingredient_search_column_view,
            get_searchable_strings=lambda: self._all_ingredient_names,
            on_result_selected=self._on_ingredient_selected,
        )
        # Place into a dialog box
        self.ingredients_editor_popup = DialogBoxView(
            title="Add Ingredient",
            parent=self.view,
        )
        lyt_ingredient_search = QVBoxLayout()
        lyt_ingredient_search.addWidget(self.ingredient_search_column_view)
        self.ingredients_editor_popup.setLayout(lyt_ingredient_search)

        # Configure the serve time popup
        self.serve_time_popup = TimeIntervalPopupView()
   
        # Configure the tag editor popup
        # Init the tag selector popup
        self.recipe_tag_selector_popup = RecipeTagSelectorPopup(parent=self.view)
        # Init the controller
        self.recipe_tag_editor_ctrl = RecipeTagEditorCtrl(
            recipe_tag_editor_view=self.view.recipe_tag_editor_view, 
            recipe_tag_selector_popup=self.recipe_tag_selector_popup,
            on_tag_added=self._on_recipe_tag_added,
            on_tag_removed=self._on_recipe_tag_removed
        )

        # Connect signals and slots
        self._connect_toolbar()
        self._connect_basic_info_fields()        
        self._connect_ingredients_editor()
        self._connect_serve_time_editor()

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
        # Clear the existing ingredients
        self.view.ingredients_editor.remove_all_ingredients()
        # Add the ingredients to the view
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
        # Clear the existing time intervals
        self.view.serve_time_intervals_editor_view.clear()
        # Add the time intervals to the view
        for interval in recipe.serve_times:
            self.view.serve_time_intervals_editor_view.add_time_interval(
                convert_datetime_interval_to_time_string_interval(interval)
            )
        # Update the recipe tag field
        self.recipe_tag_editor_ctrl.update_recipe_tags(recipe.tags)

    def _cache_recipe_names(self) -> None:
        """Cache the recipe names."""
        with DatabaseService() as db_service:
            self._recipe_names = db_service.fetch_all_recipe_names()

    def _cache_ingredient_names(self) -> None:
        """Cache the ingredient names."""
        with DatabaseService() as db_service:
            self._all_ingredient_names = db_service.fetch_all_ingredient_names()

    def _on_recipe_selected(self, list_item: QListWidgetItem) -> None:
        """Handle a recipe being selected."""
        recipe_name = list_item.text()
        # Fetch the recipe from the database
        with DatabaseService() as db_service:
            recipe = db_service.fetch_recipe_by_name(recipe_name)
        # Load the recipe into the editor
        self.load_recipe_instance(recipe)

    def _on_add_recipe_clicked(self) -> None:
        """Handle the add recipe button being clicked."""
        # Load a new recipe instance
        self.load_recipe_instance(Recipe())
        # Recache recipe names
        self._cache_recipe_names()
        # Open the name editor view
        self.recipe_name_editor_view.clear()
        self.recipe_name_editor_view.show()

    def _on_delete_recipe_clicked(self) -> None:
        """Handler for deleting a recipe."""
        # If no recipe is selected, show the info box to tell the user
        # to select a recipe
        if self.view.recipe_search.selected_result is None:
            ok_dialog_box_view = OkDialogBoxView(
                title="No Recipe Selected",
                message="Please select a recipe to delete.",
                parent=self.view
            )
            ok_dialog_box_view.okClicked.connect(lambda: ok_dialog_box_view.close())
            ok_dialog_box_view.show()
        else:
            # Grab the recipe name from the view
            recipe_name = self.view.recipe_search.selected_result.text()
            # Otherwise, show a confirmation dialog
            confirm_dialog_box_view = ConfirmDialogBoxView(
                title="Delete Recipe",
                message=f"Are you sure you want to delete the recipe '{recipe_name}'?",
                parent=self.view
            )
            # Define confirm function
            def on_confirm():
                self._on_delete_recipe(recipe_name)
                confirm_dialog_box_view.close()
            # Connect the confirm and cancel signals
            confirm_dialog_box_view.confirmClicked.connect(on_confirm)
            confirm_dialog_box_view.cancelClicked.connect(
                lambda: confirm_dialog_box_view.close()
            )
            confirm_dialog_box_view.show()

    def _on_delete_recipe(self, recipe_name: str) -> None:
        """Handler for deleting a recipe."""
        # Fetch the recipe from the database
        with DatabaseService() as db_service:
            recipe = db_service.fetch_recipe_by_name(recipe_name)
            db_service.delete_recipe_by_name(recipe_name)
            db_service.commit()
        # Recache the recipe names
        self._cache_recipe_names()
        # Update the view with the new recipe names
        self.search_column_ctrl.reset_search()
        # Clear the recipe editor
        self.load_recipe_instance(Recipe())

    def _on_save_to_json_button_clicked(self) -> None:
        """Handle the save to JSON button being clicked."""
        # Open the name required popup if the name is empty
        if self.recipe.name is None or self.recipe.name.strip() == "":
            name_required_popup = OkDialogBoxView(
                title="Name Required",
                message="Please enter a name for the recipe.",
                parent=self.view
            )
            name_required_popup.okClicked.connect(lambda: name_required_popup.close())
            name_required_popup.show()
            return None
        # Create a .json datafile representing the recipe
        recipe_data = convert_recipe_to_json(self.recipe)
        # If the datafile already exists, ask to confirm overwriting
        if recipe_datafile_exists(convert_to_snake_case(self.recipe.name)):
            overwrite_popup = ConfirmDialogBoxView(
                title="File Exists",
                message="A file with this name already exists. Overwrite?",
                parent=self.view
            )
            # Define the overwrite function
            def on_overwrite():
                save_recipe_datafile(recipe_data, overwrite=True)
                overwrite_popup.close()               
            # Connect the confirm and cancel signals
            overwrite_popup.confirmClicked.connect(on_overwrite)
            overwrite_popup.cancelClicked.connect(lambda: overwrite_popup.close())
            overwrite_popup.show()
        else:
            # Save the recipe datafile
            save_recipe_datafile(recipe_data)

    def _on_recipe_name_changed(self, name: str) -> None:
        """Handle the recipe name being changed."""
        # If the name is not whitespace
        if self.recipe_name_editor_view.name_is_set:
            # Check if the name is in the cached list of ingredient names
            if self.recipe_name_editor_view.name in self._recipe_names:
                # Show the name unavailable message
                self.recipe_name_editor_view.show_name_unavailable()
                # Disable the OK button
                self.recipe_name_editor_view.disable_ok_button()
            else:
                # Show the name available message
                self.recipe_name_editor_view.show_name_available()
                # Enable the OK button
                self.recipe_name_editor_view.enable_ok_button()
        else:
            # Show the instructions message
            self.recipe_name_editor_view.show_instructions()
            # Disable the OK button
            self.recipe_name_editor_view.disable_ok_button()

    def _on_recipe_name_accepted(self, name:str) -> None:
        """Handle the recipe name being accepted."""
        # Set the name on the recipe
        self.recipe.name = name
        # If the recipe has an ID, update it in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()
        else:
            # Otherwise, insert it into the database
            with DatabaseService() as db_service:
                self.recipe.id = db_service.insert_new_recipe(self.recipe)
                db_service.commit()
        # Update the name on the view
        self.view.update_name(self.recipe.name)
        # Recache the recipe names
        self._cache_recipe_names()
        # Update the view with any new recipe names
        self.search_column_ctrl.reset_search()
        # Clear the recipe name editor dialog
        self.recipe_name_editor_view.clear()
        # Hide the name editor dialog
        self.recipe_name_editor_view.hide()

    def _on_recipe_name_edit_cancelled(self) -> None:
        """Handle the recipe name edit being cancelled."""
        # Clear the recipe name editor dialog
        self.recipe_name_editor_view.clear()
        # Hide the name editor dialog
        self.recipe_name_editor_view.hide()

    def _on_recipe_description_changed(self, description:str|None) -> None:
        """Handle the recipe description being changed."""
        # Update the description on the model
        self.recipe.description = description
        # Update the description in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()

    def _on_recipe_instructions_changed(self, instructions:str|None) -> None:
        """Handle the recipe instructions being changed."""
        # Update the instructions on the model
        self.recipe.instructions = instructions
        # Update the instructions in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()

    def _on_add_ingredient_clicked(self) -> None:
        """Handle the add ingredient button being clicked."""
        # Recache the ingredient names
        self._cache_ingredient_names()
        # Show the ingredient search popup
        self.ingredient_search_column_view.clear_search_term()
        self.ingredients_editor_popup.show()

    def _on_ingredient_selected(self, list_item: QListWidgetItem) -> None:
        """Handler for an ingredient being selected"""
        ingredient_name = list_item.text()
        # Grab the id for the ingredient name
        with DatabaseService() as db_service:
            ingredient = db_service.fetch_ingredient_by_name(ingredient_name)
        # If the ingredient is already in the recipe
        if ingredient.id in self.recipe.ingredient_quantities:
            # Show an error popup
            error_popup = OkDialogBoxView(
                title="Ingredient Already Added",
                message="This ingredient is already in the recipe.",
                parent=self.view
            )
            error_popup.okClicked.connect(lambda: error_popup.close())
            error_popup.show()
            return None
        # Add the ingredient quantity to the view
        self.view.ingredients_editor.add_ingredient_quantity(
            ingredient_name=ingredient_name,
            ingredient_id=ingredient.id, # type: ignore
            ingredient_quantity_value=0.0,
            ingredient_quantity_unit="g",
            ingredient_quantity_upper_tol=0.0,
            ingredient_quantity_lower_tol=0.0,
        )
        # Add the ingredient quantity to the recipe
        ingredient_quantity = IngredientQuantity(
            ingredient=ingredient,
            qty_value=0.0,
            qty_unit="g",
            qty_utol=0.0,
            qty_ltol=0.0,
        )
        self.recipe.add_ingredient_quantity(ingredient_quantity)
        # Update the recipe in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()

    def _on_remove_ingredient_clicked(self) -> None:
        """Handle the remove ingredient button being clicked."""
        # If no ingredient is selected, show a popup to inform the user
        if not self.view.ingredients_editor.ingredient_is_selected:
            no_ingredient_selected_popup = OkDialogBoxView(
                title="No Ingredient Selected",
                message="Please select an ingredient to remove.",
                parent=self.view
            )
            no_ingredient_selected_popup.okClicked.connect(
                lambda: no_ingredient_selected_popup.close()
            )
            no_ingredient_selected_popup.show()
            return None
        else:
            # Get the selected ingredient ID
            ingredient_id = self.view.ingredients_editor.selected_ingredient_id
            assert ingredient_id is not None
            # Remove the ingredient from the recipe
            self.recipe.remove_ingredient_quantity(ingredient_id)
            # Update the ingredients in the view
            self.view.ingredients_editor.remove_ingredient_quantity(ingredient_id)
            # Update the recipe in the database
            if self.recipe.id is not None:
                with DatabaseService() as db_service:
                    db_service.update_recipe(self.recipe)
                    db_service.commit()

    def _on_ingredient_qty_changed(self, ingredient_id: int, qty: float) -> None:
        """Handle the ingredient quantity being changed."""
        # Update the ingredient quantity in the recipe
        self.recipe.update_ingredient_quantity_value(ingredient_id, qty)
        # Update the recipe in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()

    def _on_ingredient_qty_unit_changed(self, ingredient_id: int, unit: str) -> None:
        """Handle the ingredient quantity unit being changed."""
        # Update the ingredient quantity unit in the recipe
        self.recipe.update_ingredient_quantity_unit(ingredient_id, unit)
        # Update the recipe in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()

    def _on_ingredient_qty_utol_changed(self, ingredient_id: int, utol: float) -> None:
        """Handle the ingredient quantity upper tolerance being changed."""
        # Update the ingredient quantity upper tolerance in the recipe
        self.recipe.update_ingredient_quantity_utol(ingredient_id, utol)
        # Update the recipe in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()

    def _on_ingredient_qty_ltol_changed(self, ingredient_id: int, ltol: float) -> None:
        """Handle the ingredient quantity lower tolerance being changed."""
        # Update the ingredient quantity lower tolerance in the recipe
        self.recipe.update_ingredient_quantity_ltol(ingredient_id, ltol)
        # Update the recipe in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()

    def _on_add_serve_time_clicked(self) -> None:
        """Handle the addition of a serve time."""
        # Show the popup
        self.serve_time_popup.show()

    def _on_remove_serve_time_clicked(self) -> None:
        """Handle the removal of a serve time."""
        # If no time interval is selected
        if not self.view.serve_time_intervals_editor_view.interval_is_selected:
            # Show an error popup
            error_popup = OkDialogBoxView(
                title="No Time Interval Selected",
                message="Please select a time interval to remove.",
                parent=self.view
            )
            error_popup.okClicked.connect(lambda: error_popup.close())
            error_popup.show()
            return None
        else:
            # Get the selected index
            index = self.view.serve_time_intervals_editor_view.selected_index
            assert index is not None
            # Create the datetime objects for the start and end times
            datetime_interval = convert_time_string_interval_to_datetime_interval(
                self.view.serve_time_intervals_editor_view.selected_time_interval_string  # type: ignore
            )
            # Remove the time interval from the recipe
            self.recipe.remove_serve_time(datetime_interval)
            # Update the serve times in the view
            self.view.serve_time_intervals_editor_view.remove_time_interval(index)
            # Remove the serve time from the database
            if self.recipe.id is not None:
                with DatabaseService() as db_service:
                    db_service.update_recipe(self.recipe)
                    db_service.commit()            

    def _on_serve_time_provided(self, start_time: str, end_time: str) -> None:
        """Handle a serve time being provided."""
        # Validate the strings as times
        try:
            # Convert the strings to datetime objects
            dt_start = datetime.strptime(start_time, "%H:%M")
            dt_end = datetime.strptime(end_time, "%H:%M")
        except ValueError:
            # Configure the error popup
            error_popup = ErrorDialogBoxView(
                title="Invalid Time",
                message="Please enter a valid time in the format HH:MM.",
                parent=self.view
            )
            error_popup.okClicked.connect(lambda: error_popup.close())
            return None
        # Add the time interval to the recipe
        self.recipe.add_serve_time((dt_start, dt_end))
        # Update the serve times in the view
        self.view.serve_time_intervals_editor_view.add_time_interval(
            convert_datetime_interval_to_time_string_interval((dt_start, dt_end))
        )
        # Update the recipe in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()
        # Hide the popup
        self.serve_time_popup.hide()

    def _on_recipe_tag_added(self, tag:str) -> None:
        """Handle a recipe tag being added."""
        # Add the tag to the recipe
        self.recipe.add_recipe_tag(tag)
        # Update the recipe in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()

    def _on_recipe_tag_removed(self, tag:str) -> None:
        """Handle a recipe tag being removed."""
        # Remove the tag from the recipe
        self.recipe.remove_recipe_tag(tag)
        # Update the recipe in the database
        if self.recipe.id is not None:
            with DatabaseService() as db_service:
                db_service.update_recipe(self.recipe)
                db_service.commit()

    def _connect_toolbar(self) -> None:
        """Connect the main button signals to their handlers"""
        self.view.addRecipeClicked.connect(self._on_add_recipe_clicked)
        self.view.deleteRecipeClicked.connect(self._on_delete_recipe_clicked)
        self.view.saveJSONClicked.connect(self._on_save_to_json_button_clicked)

    def _connect_basic_info_fields(self) -> None:
        """Connect the signals and slots for the recipe editor."""
        # Connect the edit name click
        self.view.editRecipeNameClicked.connect(self.recipe_name_editor_view.show)
        # Connect the recipe description changed signal
        self.view.txt_recipe_description.lostFocus.connect(
            self._on_recipe_description_changed
        )
        # Connect the recipe instructions changed signal
        self.view.textbox_recipe_instructions.lostFocus.connect(
            self._on_recipe_instructions_changed
        )

    def _connect_ingredients_editor(self) -> None:
        """Initialise the ingredients editor views."""
        self.view.ingredients_editor.addIngredientClicked.connect(
            self._on_add_ingredient_clicked
        )
        self.view.ingredients_editor.removeIngredientClicked.connect(
            self._on_remove_ingredient_clicked
        )
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
from codiet.db.database_service import DatabaseService
from codiet.utils.search import filter_text
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.dialog_box_views import ErrorDialogBoxView, ConfirmDialogBoxView, EntityNameDialogView
from codiet.controllers.search_column_ctrl import SearchColumnCtrl
from codiet.controllers.entity_name_dialog_ctrl import EntityNameDialogCtrl
from codiet.models.ingredients import Ingredient


class IngredientEditorCtrl:
    def __init__(self, view: IngredientEditorView):
        self.view = view  # reference to the view

        # Create an empty ingredient instance
        with DatabaseService() as db_service:
            self.ingredient = db_service.create_empty_ingredient()

        # Init the anciliarry views
        self.error_popup = ErrorDialogBoxView(parent=self.view)
        self.info_popup = ErrorDialogBoxView(parent=self.view)
        self.delete_ingredient_confirmation_popup = ConfirmDialogBoxView(
            message="Are you sure you want to delete this ingredient?",
            title="Delete Ingredient",
            parent=self.view,
        )
        self.delete_ingredient_selection_needed_popup = ErrorDialogBoxView(
            message="Please select an ingredient to delete.",
            title="No Ingredient Selected",
            parent=self.view,
        )
        self.ingredient_name_editor_dialog = EntityNameDialogView(
            entity_name="Ingredient", 
            parent=self.view
        )

        # Cache searchable lists
        self._leaf_nutrient_names: list[str] = []
        self._ingredient_names: list[str] = []
        self._cache_leaf_nutrient_names()
        self._cache_ingredient_names()

        # Connect the module controllers
        self.search_column_ctrl = SearchColumnCtrl(
            view=self.view.ingredient_search,
            get_data=lambda: self._ingredient_names,
            on_result_selected=self._on_ingredient_selected,
        )
        self.ingredient_name_editor_ctrl = EntityNameDialogCtrl(
            view=self.ingredient_name_editor_dialog,
            check_name_available=lambda name: name not in self._ingredient_names,
            on_name_accepted=self._on_ingredient_name_accepted,
        )

        # Connect the handler functions to the view signals
        self._connect_toolbar()
        self._connect_delete_ingredient_dialog()
        self._connect_basic_info_editors()
        self._connect_cost_editor()
        self._connect_bulk_editor()
        self._connect_flag_editor()
        self.view.txt_gi.textChanged.connect(self._on_gi_value_changed)
        self._connect_nutrient_editor()

    @property
    def leaf_nutrient_names(self) -> list[str]:
        """Return a list of leaf nutrient names."""
        # If there are no leaf ingredients cached
        if len(self._leaf_nutrient_names) == 0:
            # Fetch the leaf nutrient names from the database
            with DatabaseService() as db_service:
                self._leaf_nutrient_names = db_service.fetch_all_leaf_nutrient_names()
        return self._leaf_nutrient_names

    def load_ingredient_instance(self, ingredient: Ingredient):
        """Set the ingredient instance to edit."""

        # Update the stored instance
        self.ingredient = ingredient

        # Update ingredient name field
        self.view.update_name(self.ingredient.name)

        # Update description field
        self.view.update_description(self.ingredient.description)

        # Update cost fields
        self.view.update_cost_value(self.ingredient.cost_value)
        self.view.update_cost_qty_value(self.ingredient.cost_qty_value)
        self.view.update_cost_qty_unit(self.ingredient.cost_qty_unit)

        # Update the bulk properties fields
        self.view.update_density_vol_value(self.ingredient.density_vol_value)
        self.view.update_density_vol_unit(self.ingredient.density_vol_unit)
        self.view.update_density_mass_value(self.ingredient.density_mass_value)
        self.view.update_density_mass_unit(self.ingredient.density_mass_unit)

        # Update the piece mass fields
        self.view.update_pc_qty_value(self.ingredient.pc_qty)
        self.view.update_pc_mass_value(self.ingredient.pc_mass_value)
        self.view.update_pc_mass_unit(self.ingredient.pc_mass_unit)

        # Set the flags
        # Remove all old flags
        self.view.flag_editor.remove_all_flags_from_list()
        # Add the new flags
        self.view.flag_editor.add_flags_to_list(list(self.ingredient.flags.keys()))
        # Update the flag selections
        self.view.flag_editor.update_flags(self.ingredient.flags)

        # Update the GI field
        self.view.update_gi(self.ingredient.gi)

        # Set the nutrients        
        # Remove all old nutrients
        self.view.nutrient_editor.remove_all_nutrients()
        # Add the new nutrients
        self.view.nutrient_editor.add_nutrients(self.leaf_nutrient_names)
        # Update their values
        self.view.nutrient_editor.update_nutrients(self.ingredient.nutrient_quantities)

    def _cache_leaf_nutrient_names(self) -> None:
        """Cache the leaf nutrient names."""
        with DatabaseService() as db_service:
            self._leaf_nutrient_names = db_service.fetch_all_leaf_nutrient_names()

    def _cache_ingredient_names(self) -> None:
        """Cache the ingredient names."""
        with DatabaseService() as db_service:
            self._ingredient_names = db_service.fetch_all_ingredient_names()

    def _on_ingredient_selected(self, ingredient_name: str) -> None:
        """Handler for selecting an ingredient."""
        # Fetch the ingredient from the database
        with DatabaseService() as db_service:
            ingredient = db_service.fetch_ingredient_by_name(ingredient_name)
        # Load the ingredient into the view
        self.load_ingredient_instance(ingredient)

    def _on_add_new_ingredient_clicked(self) -> None:
        """Handler for adding a new ingredient."""
        # Create a new ingredient instance
        with DatabaseService() as db_service:
            ingredient = db_service.create_empty_ingredient()
        # Load the fresh instance into the UI
        self.load_ingredient_instance(ingredient)
        # Open the create new ingredient dialog box
        self.ingredient_name_editor_dialog.clear()
        self.ingredient_name_editor_dialog.show()        

    def _on_delete_ingredient_clicked(self) -> None:
        """Handler for deleting an ingredient."""
        # If no ingredient is selected, show the info box to tell the user
        # to select an ingredient.
        if self.view.ingredient_search.result_is_selected is False:
            self.delete_ingredient_selection_needed_popup.show()
        else:
            # Set the ingredient name in the confirmation dialog
            self.delete_ingredient_confirmation_popup.message = (
                f"Are you sure you want to delete {self.view.ingredient_search.selected_result}?"
            )
            # Show the confirmation dialog
            self.delete_ingredient_confirmation_popup.show()

    def _on_confirm_delete_ingredient_clicked(self) -> None:
        """Handler for confirming the deletion of an ingredient."""
        # Grab the selected ingredient name from the search widget
        ingredient_name = self.view.ingredient_search.selected_result
        # Delete the ingredient from the database
        with DatabaseService() as db_service:
            db_service.delete_ingredient_by_name(ingredient_name) # type: ignore
            db_service.commit()
        # Recache the ingredient names
        self._cache_ingredient_names()
        # Reset the search pane
        self.view.ingredient_search.update_results_list(self._ingredient_names)
        # Close the confirmation dialog
        self.delete_ingredient_confirmation_popup.hide()

    def _on_cancel_delete_ingredient_clicked(self) -> None:
        """Handler for cancelling the deletion of an ingredient."""
        # Hide the confirmation dialog
        self.delete_ingredient_confirmation_popup.hide()

    def _on_edit_ingredient_name_clicked(self) -> None:
        """Handler for editing the ingredient name."""
        # Clear the box
        self.ingredient_name_editor_dialog.clear()
        # If the ingredient has a name already, write it into the box
        if self.ingredient.name is not None:
            self.ingredient_name_editor_dialog.name = self.ingredient.name
        # Show the dialog
        self.ingredient_name_editor_dialog.show()

    def _on_ingredient_name_accepted(self, name:str) -> None:
        """Handler for accepting the new ingredient name."""
        # Set the name on the ingredient
        self.ingredient.name = self.ingredient_name_editor_dialog.name
        # If the ingredient has an id already, then we must be updating
        if self.ingredient.id is not None:
            with DatabaseService() as db_service:
                db_service.update_ingredient(self.ingredient)
                db_service.commit()
        else:
            with DatabaseService() as db_service:
                self.ingredient.id = db_service.insert_new_ingredient(self.ingredient)
                db_service.commit()
        # Update the name on the view
        self.view.update_name(self.ingredient.name)
        # Recache the ingredient names
        self._cache_ingredient_names()
        # Reset the search pane
        self.view.ingredient_search.clear_search_term()
        self.view.ingredient_search.update_results_list(self._ingredient_names)
        # Clear the new ingredient dialog
        self.ingredient_name_editor_dialog.clear()
        # Hide the new ingredient dialog
        self.ingredient_name_editor_dialog.hide()

    def _on_ingredient_description_changed(self, description: str):
        """Handler for changes to the ingredient description."""
        # Update the ingredient description
        self.ingredient.description = description

    def _on_ingredient_cost_value_changed(self, value: float|None):
        """Handler for changes to the ingredient cost."""
        # Update the ingredient cost
        self.ingredient.cost_value = value

    def _on_ingredient_cost_quantity_changed(self, value: float|None):
        """Handler for changes to the ingredient quantity associated with the cost data."""
        # Update the ingredient cost quantity
        self.ingredient.cost_qty_value = value

    def _on_ingredient_cost_qty_unit_changed(self, unit: str):
        """Handler for changes to the ingredient cost unit."""
        # Update the ingredient cost unit
        self.ingredient.cost_qty_unit = unit

    def _on_ingredient_density_vol_value_changed(self, value: float|None):
        """Handler for changes to the ingredient density volume value."""
        # Update the ingredient density volume value
        self.ingredient.density_vol_value = value

    def _on_ingredient_density_vol_unit_changed(self, value: str):
        """Handler for changes to the ingredient density volume unit."""
        # Update the ingredient density volume unit
        self.ingredient.density_vol_unit = value

    def _on_ingredient_density_mass_value_changed(self, value: float|None):
        """Handler for changes to the ingredient density mass value."""
        # Update the ingredient density mass value
        self.ingredient.density_mass_value = value

    def _on_ingredient_density_mass_unit_changed(self, value: str):
        """Handler for changes to the ingredient density mass unit."""
        # Update the ingredient density mass unit
        self.ingredient.density_mass_unit = value

    def _on_ingredient_num_pieces_changed(self, value: float|None):
        """Handler for changes to the ingredient piece count."""
        # Update the ingredient piece count
        self.ingredient.pc_qty = value

    def _on_ingredient_pc_mass_value_changed(self, value: float|None):
        """Handler for changes to the ingredient piece mass value."""
        # Update the ingredient piece mass value
        self.ingredient.pc_mass_value = value

    def _on_ingredient_pc_mass_unit_changed(self, value: str):
        """Handler for changes to the ingredient piece mass unit."""
        # Update the ingredient piece mass unit
        self.ingredient.pc_mass_unit = value

    def _on_flag_changed(self, flag_name: str, flag_value: bool):
        """Handler for changes to the ingredient flags."""
        # Update the ingredient flags
        self.ingredient.set_flag(flag_name, flag_value)

    def _on_select_all_flags_clicked(self):
        """Handler for selecting all flags."""
        # Select all flags on ingredient
        self.ingredient.set_all_flags_true()
        # Select all flags on the view
        self.view.flag_editor.set_all_flags_true()

    def _on_deselect_all_flags_clicked(self):
        """Handler for deselecting all flags."""
        # Deselect all flags on ingredient
        self.ingredient.set_all_flags_false()
        # Deselect all flags on the view
        self.view.flag_editor.set_all_flags_false()

    def _on_invert_selection_flags_clicked(self):
        """Handler for inverting the selected flags."""
        # For each flag
        for flag in self.ingredient.flags:
            # Invert the flag on the ingredient
            self.ingredient.set_flag(flag, not self.ingredient.flags[flag])
        # Invert on the view
        self.view.flag_editor.invert_flags()

    def _on_clear_selection_flags_clicked(self):
        """Handler for clearing the selected flags."""
        # Clear all flags on the ingredient
        self.ingredient.set_all_flags_false()
        # Clear all flags on the view
        self.view.flag_editor.set_all_flags_false()

    def _on_gi_value_changed(self, value:float|None):
        """Handler for changes to the ingredient GI value."""
        # Update the ingredient GI value
        self.ingredient.gi = value

    def _on_nutrient_filter_changed(self, search_term: str):
        """Handler for changes to the nutrient filter."""
        # Clear the nutrient editor
        self.view.nutrient_editor.remove_all_nutrients()
        # If the search term is empty
        if search_term.strip() == "":
            # Add all leaf nutrients back into the view
            for nutrient_name in self.leaf_nutrient_names:
                self.view.nutrient_editor.add_nutrient(nutrient_name)
            # Populate with the nutrient quantities from the ingredient instance
            self.view.nutrient_editor.update_nutrients(self.ingredient.nutrient_quantities)
        else:
            # Get the filtered list of nutrients
            filtered_nutrients = filter_text(search_term, self.leaf_nutrient_names, 3)
            # Add each of the filtered nutrients into the view
            for nutrient_name in filtered_nutrients:
                self.view.nutrient_editor.add_nutrient(nutrient_name)
            # Populate with the nutrient quantities from the ingredient instance
            for nutrient_name in filtered_nutrients:
                self.view.nutrient_editor.update_nutrient(
                    nutrient_name, self.ingredient.nutrient_quantities[nutrient_name]
                )

    def _on_nutrient_filter_cleared(self):
        """Handler for clearing the nutrient filter."""
        # Clear the text from the search filter
        self.view.nutrient_editor.search_term_widget.clear()
        # Clear the nutrient editor
        self.view.nutrient_editor.remove_all_nutrients()
        # Add all leaf nutrients back into the view
        for nutrient_name in self.leaf_nutrient_names:
            self.view.nutrient_editor.add_nutrient(nutrient_name)

    def _on_nutrient_mass_changed(self, nutrient_name: str, mass: float | None):
        """Handler for changes to the nutrient mass."""
        # Grab the nutrient quantity from the ingredient
        nutrient_quantity = self.ingredient.nutrient_quantities[nutrient_name]
        # Update the nutrient mass
        nutrient_quantity.nutrient_mass = mass

    def _on_nutrient_mass_units_changed(self, nutrient_name: str, units: str):
        """Handler for changes to the nutrient mass units."""
        # Grab the nutrient quantity from the ingredient
        nutrient_quantity = self.ingredient.nutrient_quantities[nutrient_name]
        # Update the nutrient mass units
        nutrient_quantity.nutrient_mass_unit = units

    def _on_nutrient_ingredient_qty_changed(self, nutrient_name: str, qty: float | None):
        """Handler for changes to the ingredient quantity defining a nutrient mass."""
        # Grab the nutrient quantity from the ingredient
        nutrient_quantity = self.ingredient.nutrient_quantities[nutrient_name]
        # Update the ingredient quantity
        nutrient_quantity.ingredient_quantity = qty

    def _on_nutrient_ingredient_qty_units_changed(self, nutrient_name: str, units: str):
        """Handler for changes to the ingredient quantity units used to define a nutrient mass."""
        # Grab the nutrient quantity from the ingredient
        nutrient_quantity = self.ingredient.nutrient_quantities[nutrient_name]
        # Update the ingredient mass units
        nutrient_quantity.ingredient_quantity_unit = units

    def _connect_delete_ingredient_dialog(self) -> None:
        """Connect the signals for the delete ingredient dialog."""
        self.delete_ingredient_confirmation_popup.confirmClicked.connect(
            self._on_confirm_delete_ingredient_clicked
        )
        self.delete_ingredient_confirmation_popup.cancelClicked.connect(
            self._on_cancel_delete_ingredient_clicked
        )
        self.delete_ingredient_selection_needed_popup.okClicked.connect(
            lambda: self.delete_ingredient_selection_needed_popup.hide()
        )

    def _connect_toolbar(self) -> None:
        """Connect the toolbar button signals."""
        self.view.addIngredientClicked.connect(self._on_add_new_ingredient_clicked)
        self.view.deleteIngredientClicked.connect(self._on_delete_ingredient_clicked)

    def _connect_basic_info_editors(self) -> None:
        """Connect the signals for the basic info editors."""
        # Connect the edit name button
        self.view.editIngredientNameClicked.connect(self._on_edit_ingredient_name_clicked)
        # Connect the description field
        self.view.ingredientDescriptionChanged.connect(
            self._on_ingredient_description_changed
        )

    def _connect_cost_editor(self) -> None:
        """Connect the signals for the cost editor."""
        # Connect the cost fields
        self.view.ingredientCostValueChanged.connect(self._on_ingredient_cost_value_changed)
        self.view.ingredientCostQuantityChanged.connect(self._on_ingredient_cost_quantity_changed)
        self.view.cmb_cost_qty_unit.currentTextChanged.connect(
            self._on_ingredient_cost_qty_unit_changed
        )

    def _connect_bulk_editor(self) -> None:
        """Connect the signals for the bulk editor."""
        # Connect the density fields
        self.view.txt_dens_vol.textChanged.connect(
            self._on_ingredient_density_vol_value_changed
        )
        self.view.cmb_dens_vol_unit.currentTextChanged.connect(
            self._on_ingredient_density_vol_unit_changed
        )
        self.view.txt_dens_mass.textChanged.connect(
            self._on_ingredient_density_mass_value_changed
        )
        self.view.cmb_dens_mass_unit.currentTextChanged.connect(
            self._on_ingredient_density_mass_unit_changed
        )

        # Connect the piece mass fields
        self.view.txt_num_pieces.textChanged.connect(
            self._on_ingredient_num_pieces_changed
        )
        self.view.txt_pc_mass_value.textChanged.connect(
            self._on_ingredient_pc_mass_value_changed
        )
        self.view.cmb_pc_mass_unit.currentTextChanged.connect(
            self._on_ingredient_pc_mass_unit_changed
        )

    def _connect_flag_editor(self) -> None:
        """Connect the signals for the flag editor."""
        # Connect the flag editor signals
        self.view.flag_editor.onFlagChanged.connect(self._on_flag_changed)
        self.view.flag_editor.onSelectAllFlagsClicked.connect(
            self._on_select_all_flags_clicked
        )
        self.view.flag_editor.onDeselectAllFlagsClicked.connect(
            self._on_deselect_all_flags_clicked
        )
        self.view.flag_editor.onInvertSelectionFlagsClicked.connect(
            self._on_invert_selection_flags_clicked
        )
        self.view.flag_editor.onClearSelectionFlagsClicked.connect(
            self._on_clear_selection_flags_clicked
        )

    def _connect_nutrient_editor(self) -> None:
        """Connect the signals for the nutrient editor."""
        self.view.nutrient_editor.nutrientFilterChanged.connect(
            self._on_nutrient_filter_changed
        )
        self.view.nutrient_editor.nutrientFilterCleared.connect(
            self._on_nutrient_filter_cleared
        )
        self.view.nutrient_editor.nutrientMassChanged.connect(
            self._on_nutrient_mass_changed
        )
        self.view.nutrient_editor.nutrientMassUnitsChanged.connect(
            self._on_nutrient_mass_units_changed
        )
        self.view.nutrient_editor.ingredientQtyChanged.connect(
            self._on_nutrient_ingredient_qty_changed
        )
        self.view.nutrient_editor.ingredientQtyUnitsChanged.connect(
            self._on_nutrient_ingredient_qty_units_changed
        )

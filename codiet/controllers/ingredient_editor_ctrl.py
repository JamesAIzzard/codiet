from codiet.db.database_service import DatabaseService
from codiet.utils.search import filter_text
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.dialog_box_views import ErrorDialogBoxView, YesNoDialogBoxView, EntityNameDialogView
from codiet.models.ingredients import Ingredient


class IngredientEditorCtrl:
    def __init__(self, view: IngredientEditorView):
        self.view = view  # reference to the view
        self.ingredient: Ingredient  # Ingredient instance

        # Init the anciliarry views
        self.error_popup = ErrorDialogBoxView(parent=self.view)
        self.yes_no_popup = YesNoDialogBoxView(parent=self.view)
        self.new_ingredient_dialog = EntityNameDialogView("Ingredient", parent=self.view)

        # Cache searchable lists
        self._leaf_nutrient_names: list[str] = []
        self._ingredient_names: list[str] = []
        self._cache_leaf_nutrient_names()
        self._cache_ingredient_names()

        # Connect the handler functions to the view signals
        self._connect_new_ingredient_dialog()
        self._connect_search_column()
        self._connect_basic_info_editors()
        self._connect_cost_editor()
        self._connect_bulk_editor()
        self._connect_flag_editor()
        self.view.txt_gi.textChanged.connect(self._on_gi_value_changed)
        self._connect_nutrient_editor()

        # Populate the search with the first 40 ingredients
        self.view.ingredient_search.update_results_list(self._ingredient_names)

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

    def _on_ingredient_search_term_changed(self, search_term: str) -> None:
        """Handler for changes to the search column."""
        # Clear the search UI
        self.view.ingredient_search.clear_results_list()
        # If the search term is empty
        if search_term.strip() == "":
            # Populate the list with all ingredient names
            self.view.ingredient_search.update_results_list(self._ingredient_names)
        else:
            # Find the 10x best matches
            best_matches = filter_text(search_term, self._ingredient_names, 10)
            # Add the best matches to the search column
            self.view.ingredient_search.update_results_list(best_matches)

    def _on_ingredient_search_term_cleared(self) -> None:
        """Handler for clearing the search term."""
        # Clear the search column
        self.view.ingredient_search.clear_results_list()
        # Clear the search term
        self.view.ingredient_search.clear_search_term()
        # Populate the list with all ingredient names
        self.view.ingredient_search.update_results_list(self._ingredient_names)

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
        self.new_ingredient_dialog.clear()
        self.new_ingredient_dialog.show()        

    def _on_new_ingredient_name_changed(self, name: str):
        """Handler for changes to the ingredient name."""
        # If the name is not whitespace
        if self.new_ingredient_dialog.name_is_set:
            # Check if the name is in the cached list of ingredient names
            if self.new_ingredient_dialog.name in self._ingredient_names:
                # Show the name unavailable message
                self.new_ingredient_dialog.show_name_unavailable()
                # Disable the OK button
                self.new_ingredient_dialog.disable_ok_button()
            else:
                # Show the name available message
                self.new_ingredient_dialog.show_name_available()
                # Enable the OK button
                self.new_ingredient_dialog.enable_ok_button()
        else:
            # Show the instructions message
            self.new_ingredient_dialog.show_instructions()
            # Disable the OK button
            self.new_ingredient_dialog.disable_ok_button()

    def _on_new_ingredient_name_accepted(self):
        """Handler for accepting the new ingredient name."""
        # TODO: Implement this
        raise NotImplementedError("Needs doing.")

    def _on_new_ingredient_name_cancelled(self):
        """Handler for cancelling the new ingredient name."""
        # Clear the new ingredient dialog
        self.new_ingredient_dialog.clear()
        # Hide the new ingredient dialog
        self.new_ingredient_dialog.hide()

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

    def _connect_new_ingredient_dialog(self) -> None:
        """Connect the signals for the new ingredient dialog."""
        self.new_ingredient_dialog.nameChanged.connect(self._on_new_ingredient_name_changed)
        self.new_ingredient_dialog.nameAccepted.connect(self._on_new_ingredient_name_accepted)
        self.new_ingredient_dialog.nameCancelled.connect(self._on_new_ingredient_name_cancelled)

    def _connect_search_column(self) -> None:
        """Connect the signals for the search column."""
        # Connect the search column
        self.view.searchTextChanged.connect(self._on_ingredient_search_term_changed)
        self.view.searchTextCleared.connect(self._on_ingredient_search_term_cleared)
        self.view.ingredientSelected.connect(self._on_ingredient_selected)
        self.view.addIngredientClicked.connect(self._on_add_new_ingredient_clicked)
        # self.view.deleteIngredientClicked.connect(self._on_remove_ingredient_clicked)
        # self.view.saveJSONClicked.connect(self._on_save_json_clicked)

    def _connect_basic_info_editors(self) -> None:
        """Connect the signals for the basic info editors."""
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

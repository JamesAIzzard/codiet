from codiet.db.database_service import DatabaseService
from codiet.utils.search import filter_text
from codiet.views.ingredient_editor_view import IngredientEditorView
from codiet.views.dialog_box_view import OkDialogBoxView, ErrorDialogBoxView
from codiet.models.ingredients import Ingredient


class IngredientEditorCtrl:
    def __init__(self, view: IngredientEditorView):
        self.view = view  # reference to the view
        self.ingredient: Ingredient  # Ingredient instance

        # Init the anciliarry views
        self.error_popup = ErrorDialogBoxView(parent=self.view)

        # Cache a list of leaf nutrients
        self.leaf_nutrient_names: list[str] = []

        # Connect the handler functions to the view signals
        self._connect_basic_info_editors()
        self._connect_cost_editor()
        self._connect_bulk_editor()
        self._connect_flag_editor()
        self.view.txt_gi.textChanged.connect(self._on_gi_value_changed)
        self._connect_nutrient_editor()
        self.view.btn_save_ingredient.pressed.connect(self._on_save_ingredient_pressed)

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
        self.view.flag_editor.update_flags(self.ingredient.flags)

        # Update the GI field
        self.view.update_gi(self.ingredient.gi)

        # Set the nutrients
        self.view.nutrient_editor.update_nutrients(self.ingredient.nutrient_quantities)
        # Re-cache the leaf nutrient names
        with DatabaseService() as db_service:
                    self.leaf_nutrient_names = db_service.fetch_all_leaf_nutrient_names()

    def _on_ingredient_name_changed(self):
        """Handler for changes to the ingredient name."""
        # Update the ingredient name
        self.ingredient.name = self.view.txt_ingredient_name.text()

    def _on_ingredient_description_changed(self):
        """Handler for changes to the ingredient description."""
        # Update the ingredient description
        self.ingredient.description = self.view.txt_description.toPlainText()

    def _on_ingredient_cost_value_changed(self):
        """Handler for changes to the ingredient cost."""
        # Update the ingredient cost
        self.ingredient.cost_value = self.view.txt_cost.text()

    def _on_ingredient_cost_quantity_changed(self):
        """Handler for changes to the ingredient quantity associated with the cost data."""
        # Update the ingredient cost quantity
        self.ingredient.cost_qty_value = self.view.txt_cost_quantity.text()

    def _on_ingredient_cost_qty_unit_changed(self):
        """Handler for changes to the ingredient cost unit."""
        # Update the ingredient cost unit
        self.ingredient.cost_qty_unit = self.view.cmb_cost_qty_unit.currentText()

    def _on_ingredient_density_vol_value_changed(self):
        """Handler for changes to the ingredient density volume value."""
        # Update the ingredient density volume value
        self.ingredient.density_vol_value = self.view.txt_dens_vol.text()

    def _on_ingredient_density_vol_unit_changed(self):
        """Handler for changes to the ingredient density volume unit."""
        # Update the ingredient density volume unit
        self.ingredient.density_vol_unit = self.view.cmb_dens_vol_unit.currentText()

    def _on_ingredient_density_mass_value_changed(self):
        """Handler for changes to the ingredient density mass value."""
        # Update the ingredient density mass value
        self.ingredient.density_mass_value = self.view.txt_dens_mass.text()

    def _on_ingredient_density_mass_unit_changed(self):
        """Handler for changes to the ingredient density mass unit."""
        # Update the ingredient density mass unit
        self.ingredient.density_mass_unit = self.view.cmb_dens_mass_unit.currentText()

    def _on_ingredient_num_pieces_changed(self):
        """Handler for changes to the ingredient piece count."""
        # Update the ingredient piece count
        self.ingredient.pc_qty = self.view.txt_num_pieces.text()

    def _on_ingredient_pc_mass_value_changed(self):
        """Handler for changes to the ingredient piece mass value."""
        # Update the ingredient piece mass value
        self.ingredient.pc_mass_value = self.view.txt_pc_mass_value.text()

    def _on_ingredient_pc_mass_unit_changed(self):
        """Handler for changes to the ingredient piece mass unit."""
        # Update the ingredient piece mass unit
        self.ingredient.pc_mass_unit = self.view.cmb_pc_mass_unit.currentText()

    def _on_flag_changed(self, flag_name: str, flag_value: bool):
        """Handler for changes to the ingredient flags."""
        # Update the ingredient flags
        self.ingredient.set_flag(flag_name, flag_value)

    def _on_select_all_flags_clicked(self):
        """Handler for selecting all flags."""
        # Select all flags on ingredient
        self.ingredient.set_all_flags_true()
        # Select all flags on the view
        self.view.flag_editor.select_all_flags()

    def _on_deselect_all_flags_clicked(self):
        """Handler for deselecting all flags."""
        # Deselect all flags on ingredient
        self.ingredient.set_all_flags_false()
        # Deselect all flags on the view
        self.view.flag_editor.deselect_all_flags()

    def _on_invert_selection_flags_clicked(self):
        """Handler for inverting the selected flags."""
        # For each flag
        for flag in self.ingredient.flags:
            # Invert the flag on the ingredient
            self.ingredient.set_flag(flag, not self.ingredient.flags[flag])
            # Invert on the view
            self.view.flag_editor.set_flag(flag, not self.ingredient.flags[flag])

    def _on_clear_selection_flags_clicked(self):
        """Handler for clearing the selected flags."""
        # Clear all flags on the ingredient
        self.ingredient.set_all_flags_false()
        # Clear all flags on the view
        self.view.flag_editor.deselect_all_flags()

    def _on_gi_value_changed(self):
        """Handler for changes to the ingredient GI value."""
        # Update the ingredient GI value
        self.ingredient.gi = self.view.txt_gi.text()

    def _on_nutrient_filter_changed(self, search_term: str):
        """Handler for changes to the nutrient filter."""
        # Clear the nutrient editor
        self.view.nutrient_editor.remove_nutrients()
        # Get the filtered list of nutrients
        filtered_nutrients = filter_text(search_term, self.leaf_nutrient_names, 3)
        # Add each of the filtered nutrients into the view
        for nutrient_name in filtered_nutrients:
            self.view.nutrient_editor.add_nutrient(nutrient_name)

    def _on_nutrient_filter_cleared(self):
        """Handler for clearing the nutrient filter."""
        # Clear the text from the search filter
        self.view.nutrient_editor.search_term_widget.clear()
        # Clear the nutrient editor
        self.view.nutrient_editor.remove_nutrients()
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

    def _on_save_ingredient_pressed(self):
        """Handler for the save ingredient button."""
        # Open the 'name required' popup if the name is empty
        if self.ingredient.name is None or self.ingredient.name.strip() == "":
            self.view.show_name_required_popup()
            return None
        # If we are saving a new ingredient (there is no ID yet)
        if self.ingredient.id is None:
            # Save it
            with DatabaseService() as db_service:
                self.ingredient.id = self.ingredient.id = (
                    db_service.insert_new_ingredient(self.ingredient)
                )
            # Open a popup to confirm the save
            self.view.show_save_confirmation_popup()
            return None
        # So the id is populated, this must be an update.
        # First fetch the name from the database which corresponds to this id.
        with DatabaseService() as db_service:
            existing_name = db_service.fetch_ingredient_name(self.ingredient.id)
        # If the name has changed
        if existing_name != self.ingredient.name:
            # Open a yes/no popup to confirm the update
            response = self.view.show_name_change_confirmation_popup()
            # If the user clicked no, return
            if response == False:
                return None
        # If the name has not changed, go ahead and update
        with DatabaseService() as db_service:
            db_service.update_ingredient(self.ingredient)
        # Open a popup to confirm the update
        self.view.show_update_confirmation_popup()

    def _connect_basic_info_editors(self):
        """Connect the signals for the basic info editors."""
        # Connect the name field
        self.view.txt_ingredient_name.textChanged.connect(
            self._on_ingredient_name_changed
        )

        # Connect the description field
        self.view.txt_description.textChanged.connect(
            self._on_ingredient_description_changed
        )

    def _connect_cost_editor(self):
        """Connect the signals for the cost editor."""
        # Connect the cost fields
        self.view.txt_cost.textChanged.connect(self._on_ingredient_cost_value_changed)
        self.view.txt_cost_quantity.textChanged.connect(
            self._on_ingredient_cost_quantity_changed
        )
        self.view.cmb_cost_qty_unit.currentTextChanged.connect(
            self._on_ingredient_cost_qty_unit_changed
        )

    def _connect_bulk_editor(self):
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

    def _connect_flag_editor(self):
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

    def _connect_nutrient_editor(self):
        """Connect the signals for the nutrient editor."""
        self.view.nutrient_editor.onNutrientFilterChanged.connect(
            self._on_nutrient_filter_changed
        )
        self.view.nutrient_editor.onNutrientFilterCleared.connect(
            self._on_nutrient_filter_cleared
        )
        self.view.nutrient_editor.onNutrientMassChanged.connect(
            self._on_nutrient_mass_changed
        )
        self.view.nutrient_editor.onNutrientMassUnitsChanged.connect(
            self._on_nutrient_mass_units_changed
        )
        self.view.nutrient_editor.onIngredientQtyChanged.connect(
            self._on_nutrient_ingredient_qty_changed
        )
        self.view.nutrient_editor.onIngredientQtyUnitsChanged.connect(
            self._on_nutrient_ingredient_qty_units_changed
        )

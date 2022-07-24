import typing

from PyQt6 import QtWidgets

import codiet
import app


class IngredientEditorCtrl(app.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create dict for nutrient editor controllers
        self.nutrient_editor_ctrls: typing.Dict[str, app.NutrientRatioEditorCtrl] = {}

        # Call out widgets for intellisense
        self.view: app.IngredientEditorView

        # Init controller for flag selector widget
        self.flag_selector_ctrl = app.FlagSelectorCtrl(
            view=self.view.wg_flag_selector,
        )

        # Init a list of all quantity unit dropdowns that need to stay up to date
        # with mass properties
        self._dynamic_unit_dropdowns: typing.List[app.CodietComboBox] = [
            self.view.cmb_cost_units,
            self.view.cmb_mass_pieces_units,
        ]

        # Initial setup on the form
        # Cache the basic mass units
        mass_units = list(codiet.get_mass_units().keys())
        vol_units = list(codiet.get_vol_units().keys())
        # Do the cost widget setup
        self.view.cmb_cost_units.add_items_once(mass_units)
        self.view.cmb_dens_mass_units.add_items_once(mass_units)
        self.view.cmb_dens_vol_units.add_items_once(vol_units)
        self.view.cmb_mass_pieces_units.add_items_once(mass_units)
        # Do the nutrients widget setup
        nutrients = codiet.get_adopted_nutrients()
        for nutrient in nutrients:
            self.add_nutrient_ratio_editor(
                nutrient_name=nutrient[0], nutrient_str=nutrient[1]
            )

        # Wire the active elements
        # Handle the save button press
        self.view.btn_save_ingredient.clicked.connect(self.on_save_ingredient)
        # Handle changes to density widget
        self.view.txt_dens_mass.textChanged.connect(self.on_dens_field_change)
        self.view.txt_dens_vol.textChanged.connect(self.on_dens_field_change)
        # Handle changes to the pc mass widget
        self.view.txt_num_pieces.textChanged.connect(self.on_pc_mass_field_change)
        self.view.txt_mass_pieces.textChanged.connect(self.on_pc_mass_field_change)

        # Set the title on the search widget
        self.view.wg_ingredient_search.set_title("Ingredient Search")

        # Load in a fresh ingredient instance
        self.ingredient = codiet.Ingredient()

    @property
    def cost_per_g(self) -> typing.Optional[float]:
        """Returns the cost per gram specified on the view."""
        # Return None if any of the required values are not specified
        if not self.view.cost_is_defined:
            return None

        # Go ahead and calculate cost per gram
        # First, calculate the cost per single unit
        cost_per_unit = (
            self.view.txt_cost.text() / self.view.txt_cost_qty.text() # type: ignore
        )

        # Get the ratio between the units
        unit_r = codiet.convert_qty_unit(
            qty=1,
            start_unit=self.view.cmb_cost_units.currentText(),
            end_unit="g",
            g_per_ml=self.g_per_ml,
            piece_mass_g=self.piece_mass_g,
        )

        # Done
        return cost_per_unit / unit_r

    @property
    def g_per_ml(self) -> typing.Optional[float]:
        """Returns the grams per ml specified on the view."""
        # Return none if any of the required values are not specified
        if self.view.dens_is_defined == False:
            return None

        # Values are specified - go ahead and calculate
        # Convert the fluid volume to mls
        vol_mls = codiet.convert_qty_unit(
            qty=self.view.txt_dens_vol.text(), # type: ignore
            start_unit=self.view.cmb_dens_vol_units.currentText(),
            end_unit="ml",
        )
        # Convert the mass volume to grams
        mass_g = codiet.convert_qty_unit(
            qty=self.view.txt_dens_mass.text(), # type: ignore
            start_unit=self.view.cmb_dens_mass_units.currentText(), 
            end_unit="g"
        )
        # Derive the ratio
        g_per_ml = mass_g / vol_mls
        return g_per_ml

    @property
    def piece_mass_g(self) -> typing.Optional[float]:
        """Returns the piece mass in grams from the view."""
        # Return None if any of the required info is missing
        if not self.view.piece_mass_is_defined:
            return None

        # OK, all the info is there, go ahead
        # Convert the total pieces mass into grams
        pcs_mass_g = codiet.convert_qty_unit(
            qty=self.view.txt_mass_pieces.text(), # type: ignore
            start_unit=self.view.cmb_mass_pieces_units.currentText(), 
            end_unit="g"
        )
        # Calc the mass of a single pc
        pc_mass_g = pcs_mass_g / self.view.txt_num_pieces.text() # type: ignore
        return pc_mass_g

    def _show_warning(self, title: str, message: str) -> None:
        """Raises a warning dialog box."""
        QtWidgets.QMessageBox.warning(self.view, title, message)

    def add_nutrient_ratio_editor(self, nutrient_name: str, nutrient_str: str) -> None:
        """Adds a nutrient ratio editor widget."""
        # If the nutrient is carbohydrate, bind to the carbohydrate
        # change handler, so we can update the GI
        carb_change_handler = None
        if nutrient_name == "carbohydrate":
            carb_change_handler = self.on_carb_ratio_change
        # Init the view
        view = app.NutrientRatioEditorView(
            nutrient_str=nutrient_str, on_nutrient_mass_change=carb_change_handler
        )
        # Init the controller
        ctrl = app.NutrientRatioEditorCtrl(view=view, nutrient_str=nutrient_str)
        # Stash the controller
        self.nutrient_editor_ctrls[nutrient_name] = ctrl
        # Add the mass dropdown the the list
        self._dynamic_unit_dropdowns.append(view.cmb_ingredient_qty_unit)
        # Add the view
        self.view.add_nutrient_widget(nutrient_name, view)

    def add_dens_units(self) -> None:
        """Adds density units to all unit fields on the form."""
        for combobox in self._dynamic_unit_dropdowns:
            combobox.add_items_once(list(codiet.get_vol_units().keys()))

    def remove_dens_units(self) -> None:
        """Removes density units to all unit fields on the form."""
        for combobox in self._dynamic_unit_dropdowns:
            combobox.remove_items(list(codiet.get_vol_units().keys()))

    def add_pc_units(self) -> None:
        """Adds piece units to all unit fields on the form."""
        for combobox in self._dynamic_unit_dropdowns:
            combobox.add_items_once(["pc"])

    def remove_pc_units(self) -> None:
        """Removes piece units from all unit fields on the form."""
        for combobox in self._dynamic_unit_dropdowns:
            combobox.remove_items(["pc"])

    def on_dens_field_change(self) -> None:
        """Handler for changes to the density field."""
        if self.view.dens_is_defined:
            self.add_dens_units()
        else:
            self.remove_dens_units()

    def on_pc_mass_field_change(self) -> None:
        """Handles changes to the piece mass field."""
        if self.view.piece_mass_is_defined:
            # Add piece units to dropdowns
            self.add_pc_units()
        else:
            # Remove piece units from dropdowns
            self.remove_pc_units()

    def on_carb_ratio_change(self) -> None:
        """Handler for carbohydrate ratio change."""
        # Grab the value from the carbohydrate widget
        carb_ratio_data = self.view.get_nutrient_ratio_data(
            nutrient_name="carbohydrate"
        )
        # If carbs are zero, then zero the gi, and prevent user messing with it
        if carb_ratio_data["nutrient_mass"] == 0:
            self.view.txt_gi.setText("0")
            self.view.txt_gi.setEnabled(False)
        # If carbs are non-zero, clear zero value from the GI, and allow user to change
        else:
            if self.view.txt_gi.text() == 0:
                self.view.txt_gi.setText("")
            self.view.txt_gi.setEnabled(True)

    def on_save_ingredient(self) -> None:
        """Click handler for save ingredient button."""
        # First check the form has been completed
        # Set title for incomplete data warnings
        warn_title = "Incomplete Data"
        # Check name has been populated
        if self.view.txt_ingredient_name.text() is None:
            self._show_warning(warn_title, "The ingredient name must be populated.")
            return
        # Check cost has been populated
        if not self.view.cost_is_defined:
            self._show_warning(
                warn_title, "The ingredient cost data must be populated."
            )
            return
        # Check nutrient data has been populated
        if not self.view.all_nutrient_fields_filled:
            self._show_warning(warn_title, "All nutrient data must be populated.")
            return

        # All seems populated, so now pass the data into the ingredient instance
        # Set the ingredient name
        self.ingredient.name = self.view.txt_ingredient_name.text()
        # Set the ingredient cost info
        self.ingredient.cost_per_ref_qty = self.view.txt_cost.text()
        self.ingredient.cost_ref_qty = self.view.txt_cost_qty.text()
        self.ingredient.cost_pref_unit = self.view.cmb_cost_units.currentText()
        # Set the ingredient density info
        self.ingredient.dens_vol_ref_qty = self.view.txt_dens_vol.text()
        self.ingredient.dens_vol_unit = self.view.cmb_dens_vol_units.currentText()
        self.ingredient.dens_mass_ref_qty = self.view.txt_dens_mass.text()
        self.ingredient.dens_mass_unit = self.view.cmb_dens_mass_units.currentText()
        # Set the ingredient piece mass info
        self.ingredient.piece_mass_ref_num = self.view.txt_num_pieces.text()
        self.ingredient.piece_mass_ref_mass = self.view.txt_mass_pieces.text()
        self.ingredient.piece_mass_ref_units = self.view.cmb_mass_pieces_units.currentText()
        # Set the ingredient flags info
        self.ingredient.flags = list(self.flag_selector_ctrl.adopted_flags.keys())
        # Set the glycaemic index info
        self.ingredient.gi = self.view.txt_gi.text()
        # Set the nutrients info
        nutrients_data = self.view.all_nutrient_ratio_data
        for nutrient_name, nutrient_data in nutrients_data.items():
            self.ingredient.nutrients[nutrient_name] = nutrient_data

        # Go ahead and save the ingredient
        codiet.save_new_ingredient(self.ingredient)

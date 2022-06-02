import typing

from PyQt6 import QtWidgets

import codiet
import app


class IngredientEditorCtrl(app.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create dict for nutrient editor controllers
        self.nutrient_editor_ctrls: typing.Dict[str, app.NutrientRatioEditorCtrl] = {}

        # Call out the view type for intellisense
        self.view: app.IngredientEditorView

        # Init controller for flag selector widget
        self.flag_selector_ctrl = app.FlagSelectorCtrl(
            view=self.view.wg_flag_selector,
        )

        # Load in a fresh ingredient instance
        self.ingredient = codiet.Ingredient()

        # Initial setup on the form
        # Cache the basic mass units
        mass_units = list(codiet.get_mass_units().keys())
        vol_units = list(codiet.get_vol_units().keys())
        # Do the cost widget setup
        app.utils.cmb_add_items_once(self.view.cmb_cost_units, mass_units)
        app.utils.cmb_add_items_once(self.view.cmb_dens_mass_units, mass_units)
        app.utils.cmb_add_items_once(self.view.cmb_dens_vol_units, vol_units)
        app.utils.cmb_add_items_once(self.view.cmb_mass_pieces_units, mass_units)
        # Do the nutrients widget setup
        nutrients = codiet.get_adopted_nutrients()
        for nutrient in nutrients:
            self.add_nutrient_ratio_editor(
                nutrient_name=nutrient[0], nutrient_str=nutrient[1]
            )

        # Wire the active elements
        # Handle the save button press
        self.view.btn_save_ingredient.clicked.connect(self.on_save_ingredient)

    @property
    def cost_per_g(self) -> typing.Optional[float]:
        """Returns the cost per gram specified on the view."""
        # Return None if any of the required values are not specified
        if self.view.cost is None or self.view.cost_qty is None:
            return None

        # OK, values are specified, so go ahead and calculate cost per gram
        # First, calculate the cost per single unit
        cost_per_unit = self.view.cost / self.view.cost_qty

        # Get the ratio between the units
        unit_r = codiet.convert_qty_unit(
            qty=1,
            start_unit=self.view.cost_units,
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
        if self.view.dens_mass is None or self.view.dens_vol is None:
            return None

        # Values are specified - go ahead and calculate
        # Convert the fluid volume to mls
        vol_mls = codiet.convert_qty_unit(
            qty=self.view.dens_vol, start_unit=self.view.dens_vol_units, end_unit="ml"
        )
        # Convert the mass volume to grams
        mass_g = codiet.convert_qty_unit(
            qty=self.view.dens_mass, start_unit=self.view.dens_mass_units, end_unit="g"
        )
        # Derive the ratio
        g_per_ml = mass_g / vol_mls
        return g_per_ml

    @property
    def piece_mass_g(self) -> typing.Optional[float]:
        """Returns the piece mass in grams from the view."""
        # Return None if any of the required info is missing
        if self.view.pc_mass is None or self.view.num_pieces is None:
            return None

        # OK, all the info is there, go ahead
        # Convert the total pieces mass into grams
        pcs_mass_g = codiet.convert_qty_unit(
            qty=self.view.pc_mass, start_unit=self.view.pc_mass_units, end_unit="g"
        )
        # Calc the mass of a single pc
        pc_mass_g = pcs_mass_g / self.view.num_pieces
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
        # Add the view
        self.view.add_nutrient_widget(nutrient_name, view)

    def on_carb_ratio_change(self) -> None:
        """Handler for carbohydrate ratio change."""
        # Grab the value from the carbohydrate widget
        carb_ratio_data = self.view.get_nutrient_ratio_data(nutrient_name="carbohydrate")
        # If carbs are zero, then zero the gi, and prevent user messing with it
        if carb_ratio_data["nutrient_mass"] == 0:
            self.view.txt_gi.setText("0")
            self.view.txt_gi.setEnabled(False)
        # If carbs are non-zero, clear zero value from the GI, and allow user to change
        else:
            if self.view.gi == 0:
                self.view.txt_gi.setText("")
            self.view.txt_gi.setEnabled(True)

    def on_save_ingredient(self) -> None:
        """Click handler for save ingredient button."""
        # First check the form has been completed
        # Set title for incomplete data warnings
        warn_title = "Incomplete Data"
        # Check name has been populated
        if self.view.name is None:
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

        # Set the ingredient name
        self.ingredient.name = self.view.name
        # Set the ingredient cost info
        self.ingredient.cost_per_ref_qty = self.view.cost
        self.ingredient.cost_ref_qty = self.view.cost_qty
        self.ingredient.cost_pref_unit = self.view.cost_units
        # Set the ingredient density info
        self.ingredient.dens_vol_ref_qty = self.view.dens_vol
        self.ingredient.dens_vol_unit = self.view.dens_vol_units
        self.ingredient.dens_mass_ref_qty = self.view.dens_mass
        self.ingredient.dens_mass_unit = self.view.dens_mass_units
        # Set the ingredient piece mass info
        self.ingredient.piece_mass_ref_num = self.view.num_pieces
        self.ingredient.piece_mass_ref_mass = self.view.pc_mass
        self.ingredient.piece_mass_ref_units = self.view.pc_mass_units
        # Set the ingredient flags info
        self.ingredient.flags = list(self.flag_selector_ctrl.adopted_flags.keys())
        # Set the glycaemic index info
        self.ingredient.gi = self.view.gi
        # Set the nutrients info
        nutrients_data = self.view.all_nutrient_ratio_data
        for nutrient_name, nutrient_data in nutrients_data.items():
            self.ingredient.nutrients[nutrient_name] = nutrient_data
        # Go ahead and save the ingredient
        codiet.save_new_ingredient(self.ingredient)

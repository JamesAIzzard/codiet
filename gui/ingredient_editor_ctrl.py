from logging import warn
import typing

from PyQt6 import QtWidgets

import gui, data, model


class IngredientEditorCtrl(gui.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create dict for nutrient editor controllers
        self.nutrient_editor_ctrls: typing.Dict[str, gui.NutrientRatioEditorCtrl] = {}

        # Call out the view type for intellisense
        self.view: gui.IngredientEditorView

        # Init controller for flag selector widget
        self.flag_selector_ctrl = gui.FlagSelectorCtrl(
            view=self.view.wg_flag_selector,
            on_flag_adoption_callback=self.on_flag_adopt,
            on_flag_removal_callback=self.on_flag_remove,
        )

        # Load in a fresh ingredient instance
        self.ingredient = model.ingredients.Ingredient()

        # Initial setup on the form
        # Cache the basic mass units
        mass_units = list(data.quantity.get_mass_units().keys())
        vol_units = list(data.quantity.get_vol_units().keys())
        # Do the cost widget setup
        gui.utils.cmb_add_items_once(
            self.view.cmb_cost_units, mass_units
        )
        # Do the bulk widget setup
        gui.utils.cmb_add_items_once(
            self.view.cmb_ref_qty_units, mass_units
        )
        gui.utils.cmb_add_items_once(
            self.view.cmb_dens_mass_units, mass_units
        )
        gui.utils.cmb_add_items_once(
            self.view.cmb_dens_vol_units, vol_units
        )
        gui.utils.cmb_add_items_once(
            self.view.cmb_mass_pieces_units, mass_units
        )      
        # Do the nutrients widget setup
        nutrients = data.nutrients.get_adopted_nutrients()
        for nutrient in nutrients:
            self.add_nutrient_ratio_editor(
                nutrient_name=nutrient[0], nutrient_str=nutrient[1]
            )

        # Wire the active elements
        self.view.btn_save_ingredient.clicked.connect(  # type: ignore
            self.on_save_ingredient
        )

    @property
    def cost_per_g(self) -> typing.Optional[float]:
        """Returns the cost per gram specified on the view."""
        # Return None if any of the required values are not specified
        if self.view.cost is None or self.view.cost_mass is None:
            return None

        # OK, values are specified, so go ahead and calculate cost per gram
        # First, calculate the cost per single unit
        cost_per_unit = self.view.cost / self.view.cost_mass

        # Get the ratio between the units
        unit_r = model.quantity.convert_qty_unit(
            qty=1,
            start_unit=self.view.cost_units,
            end_unit='g',
            g_per_ml=self.g_per_ml,
            piece_mass_g=self.piece_mass_g
        )

        # Done
        return cost_per_unit/unit_r

    @property
    def g_per_ml(self) -> typing.Optional[float]:
        """Returns the grams per ml specified on the view."""
        # Return none if any of the required values are not specified
        if self.view.dens_mass is None or self.view.dens_vol is None:
            return None

        # Values are specified - go ahead and calculate
        # Convert the fluid volume to mls
        vol_mls = model.quantity.convert_qty_unit(
            qty=self.view.dens_vol,
            start_unit=self.view.dens_vol_units,
            end_unit="ml"
        )
        # Convert the mass volume to grams
        mass_g = model.quantity.convert_qty_unit(
            qty=self.view.dens_mass,
            start_unit=self.view.dens_mass_units,
            end_unit='g'
        )
        # Derive the ratio
        g_per_ml = mass_g/vol_mls
        return g_per_ml

    @property
    def piece_mass_g(self) -> typing.Optional[float]:
        """Returns the piece mass in grams from the view."""
        # Return None if any of the required info is missing
        if self.view.pc_mass is None or self.view.num_pieces is None:
            return None
        
        # OK, all the info is there, go ahead
        # Convert the total pieces mass into grams
        pcs_mass_g = model.quantity.convert_qty_unit(
            qty=self.view.pc_mass,
            start_unit=self.view.pc_mass_units,
            end_unit='g'
        )
        # Calc the mass of a single pc
        pc_mass_g = pcs_mass_g / self.view.num_pieces
        return pc_mass_g


    def _show_warning(self, title:str, message:str) -> None:
        """Raises a warning dialog box."""
        QtWidgets.QMessageBox.warning(self.view, title, message)        

    def add_nutrient_ratio_editor(self, nutrient_name: str, nutrient_str: str) -> None:
        """Adds a nutrient ratio editor widget."""
        # Create the view
        view = gui.NutrientRatioEditorView(nutrient_str=nutrient_str)
        ctrl = gui.NutrientRatioEditorCtrl(view=view, nutrient_str=nutrient_str)
        self.nutrient_editor_ctrls[nutrient_name] = ctrl
        self.view.add_nutrient_widget(view)

    def on_flag_adopt(self, flag_str: str) -> None:
        """Handler function for flag adoption."""
        pass

    def on_flag_remove(self, flag_str: str) -> None:
        """Hander function for flag removal."""
        pass

    def on_save_ingredient(self) -> None:
        """Click handler for save ingredient button."""
        # Set title for warning boxes
        warn_title = "Incomplete Data"

        # Check name has been populated
        if self.view.name is None:
            self._show_warning(warn_title, "The ingredient name must be populated.")
            return
        # Check cost has been populated
        if self.cost_per_g is None:
            self._show_warning(warn_title, "The ingredient cost data must be populated.")
            return

        # Grab the name from the ingredient lineedit
        self.ingredient.name = self.view.name
        self.ingredient.cost_per_g = self.cost_per_g
        print(self.ingredient.cost_per_g)

        # Hmmmm, not sure about the best way to do this just yet.
        # data.save_ingredient(self.ingredient)
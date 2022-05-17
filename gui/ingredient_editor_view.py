import typing

from PyQt6 import QtWidgets, uic

import gui


class IngredientEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out active elements for intellisense
        self.wg_flags: QtWidgets.QGroupBox
        self.txt_ingredient_name: QtWidgets.QLineEdit
        self.txt_cost: QtWidgets.QLineEdit
        self.txt_cost_qty: QtWidgets.QLineEdit
        self.cmb_cost_units: QtWidgets.QComboBox
        self.txt_dens_vol: QtWidgets.QLineEdit
        self.cmb_dens_vol_units: QtWidgets.QComboBox
        self.txt_dens_mass: QtWidgets.QLineEdit
        self.cmb_dens_mass_units: QtWidgets.QComboBox
        self.txt_num_pieces: QtWidgets.QLineEdit
        self.txt_mass_pieces: QtWidgets.QLineEdit
        self.cmb_mass_pieces_units: QtWidgets.QComboBox
        self.txt_gi: QtWidgets.QLineEdit
        self.scl_nutrients: QtWidgets.QWidget
        self.lyt_flags: QtWidgets.QVBoxLayout
        self.lyt_nutrients: QtWidgets.QVBoxLayout
        self.btn_save_ingredient:QtWidgets.QPushButton

        # Create a dict to store the nutrient editor views
        self.nutrient_editor_views: typing.Dict[str, gui.NutrientRatioEditorView] = {}

        # Load in the ui file
        uic.load_ui.loadUi("gui/ingredient_editor.ui", self)

        # Set the validators to catch basic errors
        self.txt_cost.setValidator(gui.PositiveFloatValidator())
        self.txt_cost_qty.setValidator(gui.PositiveFloatValidator())
        self.txt_dens_vol.setValidator(gui.PositiveFloatValidator())
        self.txt_dens_mass.setValidator(gui.PositiveFloatValidator())
        self.txt_num_pieces.setValidator(gui.PositiveFloatValidator())
        self.txt_mass_pieces.setValidator(gui.PositiveFloatValidator())
        self.txt_gi.setValidator(gui.PositiveFloatValidator())

        # Build the flag editor widget
        self.wg_flag_selector = gui.FlagSelectorView()
        self.lyt_flags.addWidget(self.wg_flag_selector)

    @property
    def name(self) -> typing.Optional[str]:
        """Returns the ingredient name from the line edit."""
        if self.txt_ingredient_name.text() == "":
            return None
        else:
            return self.txt_ingredient_name.text()

    @property
    def cost_is_defined(self) -> bool:
        """Returns True/False to indicate if the cost fields are defined."""
        if self.txt_cost.text() == "":
            return False
        if self.txt_cost_qty.text() == "":
            return False
        return True

    @property
    def cost(self) -> typing.Optional[float]:
        """Returns the cost from the line edit.
        Validation prevents the user entering non-numeric values
        or numeric values that are zero or less.
        """
        if self.txt_cost.text() == "":
            return None
        else:
            return float(self.txt_cost.text())

    @property
    def cost_qty(self) -> typing.Optional[float]:
        """Returns the cost mass from the line edit."""
        if self.txt_cost_qty.text() == "":
            return None
        else:
            return float(self.txt_cost_qty.text())

    @property
    def cost_units(self) -> str:
        """Returns the cost units from the combobox."""
        return self.cmb_cost_units.currentText()

    @property
    def dens_vol(self) -> typing.Optional[float]:
        """Returns the density volume from the line edit."""
        if self.txt_dens_vol.text() == "":
            return None
        else:
            return float(self.txt_dens_vol.text())

    @property
    def dens_vol_units(self) -> str:
        """Returns the volume units from the density combobox."""
        return self.cmb_dens_vol_units.currentText()

    @property
    def dens_mass(self) -> typing.Optional[float]:
        """Returns the density mass from the line edit."""
        if self.txt_dens_mass.text() == "":
            return None
        else:
            return float(self.txt_dens_mass.text())

    @property
    def dens_mass_units(self) -> str:
        """Returns the mass units from the density combobox."""
        return self.cmb_dens_mass_units.currentText()

    @property
    def num_pieces(self) -> typing.Optional[float]:
        """Returns the number of pieces from the line edit."""
        if self.txt_num_pieces.text() == "":
            return None
        else:
            return float(self.txt_num_pieces.text())

    @property
    def pc_mass(self) -> typing.Optional[float]:
        """Returns the piece mass value from the line edit."""
        if self.txt_mass_pieces.text() == "":
            return None
        else:
            return float(self.txt_mass_pieces.text())

    @property
    def pc_mass_units(self) -> str:
        """Returns the piece mass units from the combobox."""
        return self.cmb_mass_pieces_units.currentText()

    @property
    def adopted_flag_names(self) -> typing.List[str]:
        """Returns a list of all of the adopted flag names on the view."""
        return self.wg_flag_selector.all_adopted_flags

    @property
    def gi(self) -> typing.Optional[float]:
        """Returns the GI value.
        This is validated to be a float \in [0, 100]
        """
        if self.txt_gi.text() == "":
            return None
        else:
            return float(self.txt_gi.text())

    @property
    def all_nutrient_fields_filled(self) -> bool:
        """Returns True/False to indicate if all the nutrients have been defined.
        Note:
            This doesn't do any checks to ensure that this is the full list of adopted nutrients.
            It just checks that all nutrient lines on the form have been populated.
        """
        for view in self.nutrient_editor_views.values():
            if not view.nutrient_ratio_defined:
                return False
        # All were defined
        return True

    # @property
    # def nutrients_data(self) -> typing.Dict[str, ]

    def add_nutrient_widget(self, nutrient_name:str, view: gui.NutrientRatioEditorView) -> None:
        """Adds a nutrient ratio editor widget view."""
        # Stash the view instance
        self.nutrient_editor_views[nutrient_name] = view
        # Insert the view
        self.lyt_nutrients.addWidget(view)

from typing import List, Optional

from PyQt6 import QtWidgets, QtGui, uic

import gui


class IngredientEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out active elements for intellisense
        self.wg_flags: QtWidgets.QGroupBox
        self.txt_ingredient_name: QtWidgets.QLineEdit
        self.txt_cost: QtWidgets.QLineEdit
        self.txt_cost_mass: QtWidgets.QLineEdit
        self.cmb_cost_units: QtWidgets.QComboBox
        self.scl_nutrients: QtWidgets.QWidget
        self.lyt_flags: QtWidgets.QVBoxLayout
        self.lyt_nutrients: QtWidgets.QVBoxLayout

        # Load in the ui file
        uic.load_ui.loadUi("gui/ingredient_editor.ui", self)

        # Set the validators to catch basic errors
        float_val = QtGui.QDoubleValidator()
        self.txt_cost.setValidator(float_val)
        self.txt_cost_mass.setValidator(float_val)

        # Build the flag editor widget
        self.wg_flag_selector = gui.FlagSelectorView()
        self.lyt_flags.addWidget(self.wg_flag_selector)

    @property
    def name(self) -> str:
        """Returns the ingredient name from the line edit."""
        return self.txt_ingredient_name.text()

    @property
    def cost(self) -> Optional[float]:
        """Returns the cost from the line edit.
        Validation prevents the user entering non-numeric values
        or numeric values that are zero or less.
        """
        if self.txt_cost.text() == "":
            return None
        else:
            return float(self.txt_cost.text())

    @property
    def cost_mass(self) -> Optional[float]:
        """Returns the cost mass from the line edit."""
        if self.txt_cost.text() == "":
            return None
        else:
            return float(self.txt_cost_mass.text())

    @property
    def cost_units(self) -> str:
        """Returns the cost units from the combobox."""
        return self.cmb_cost_units.currentText()

    def set_cost_units(self, units: List[str]) -> None:
        """Sets the units in the cost units box."""
        self.cmb_cost_units.clear()
        self.cmb_cost_units.addItems(units)

    def add_nutrient_widget(self, view: gui.NutrientRatioEditorView) -> None:
        """Adds a nutrient ratio editor widget view."""
        self.lyt_nutrients.addWidget(view)

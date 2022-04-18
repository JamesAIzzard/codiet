from typing import List

from PyQt6 import QtWidgets, uic

import gui


class IngredientEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out active elements for intellisense
        self.wg_flags: QtWidgets.QGroupBox
        self.cmb_cost_units: QtWidgets.QComboBox
        self.scl_nutrients: QtWidgets.QWidget
        self.lyt_flags: QtWidgets.QVBoxLayout
        self.lyt_nutrients: QtWidgets.QVBoxLayout

        # Load in the ui file
        uic.load_ui.loadUi("gui/ingredient_editor.ui", self)

        # Build the flag editor widget
        self.wg_flag_selector = gui.FlagSelectorView()
        self.lyt_flags.addWidget(self.wg_flag_selector)

    def set_cost_units(self, units: List[str]) -> None:
        """Sets the units in the cost units box."""
        self.cmb_cost_units.clear()
        self.cmb_cost_units.addItems(units)

    def add_nutrient_widget(self, view: gui.NutrientRatioEditorView) -> None:
        """Adds a nutrient ratio editor widget view."""
        self.lyt_nutrients.addWidget(view)

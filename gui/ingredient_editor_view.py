from typing import List

from PyQt6 import QtWidgets, uic

import gui

class IngredientEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out active elements for intellisense
        self.wg_flags: QtWidgets.QGroupBox
        self.cmb_cost_units:  QtWidgets.QComboBox

        # Load in the ui file
        uic.load_ui.loadUi('gui/ingredient_editor.ui', self)

        # Build the flag editor widget
        self.wg_flag_selector = gui.FlagSelectorView()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.wg_flag_selector)
        vbox.setContentsMargins(0,0,0,0)
        self.wg_flags.setLayout(vbox)

    def set_cost_units(self, units:List[str]) -> None:
        """Sets the units in the cost units box."""
        self.cmb_cost_units.clear()
        self.cmb_cost_units.addItems(units)        
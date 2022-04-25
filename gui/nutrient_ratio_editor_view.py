from typing import List

from PyQt6 import QtWidgets, uic

class NutrientRatioEditorView(QtWidgets.QWidget):
    def __init__(self,
        nutrient_str:str,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Call out active elements for intelllisense
        self.lbl_nutrient_name: QtWidgets.QLabel
        self.txt_nutrient_mass: QtWidgets.QLineEdit
        self.cmb_nutrient_mass_unit: QtWidgets.QComboBox
        self.txt_ingredient_mass: QtWidgets.QLineEdit
        self.cmb_ingredient_qty_unit: QtWidgets.QComboBox

        # Bring the ui file in
        uic.load_ui.loadUi('gui/nutrient_ratio_editor.ui', self)

        # Update the nutrient name label
        self.set_nutrient_name(nutrient_str)

    def set_nutrient_name(self, nutrient_name: str) -> None:
        """Sets the nutrient name on the widget."""
        self.lbl_nutrient_name.setText(f"{nutrient_name}:")
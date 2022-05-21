import typing

from PyQt6 import QtWidgets, uic

import gui


class NutrientRatioEditorView(QtWidgets.QWidget):
    def __init__(
        self,
        nutrient_str: str,
        on_nutrient_mass_change: typing.Optional[typing.Callable[[], None]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # Call out active elements for intelllisense
        self.lbl_nutrient_name: QtWidgets.QLabel
        self.txt_nutrient_mass: QtWidgets.QLineEdit
        self.cmb_nutrient_mass_unit: QtWidgets.QComboBox
        self.txt_ingredient_qty: QtWidgets.QLineEdit
        self.cmb_ingredient_qty_unit: QtWidgets.QComboBox

        # Bring the ui file in
        uic.load_ui.loadUi("gui/nutrient_ratio_editor.ui", self)

        # Add positive float validator to numerical input
        self.txt_ingredient_qty.setValidator(gui.PositiveFloatValidator())
        self.txt_nutrient_mass.setValidator(gui.PositiveFloatValidator())

        # Update the nutrient name label
        self.set_nutrient_name(nutrient_str)

        # Bind nutrient mass change handler if passed
        if on_nutrient_mass_change is not None:
            self.txt_nutrient_mass.textChanged.connect(on_nutrient_mass_change)

    @property
    def nutrient_ratio_defined(self) -> bool:
        """Returns True/False to indicate if the fields are populated."""
        if self.nutrient_mass is None or self.ingredient_qty is None:
            return False
        else:
            return True

    @property
    def nutrient_mass(self) -> typing.Optional[float]:
        """Returns the nutrient mass value."""
        if self.txt_nutrient_mass.text() == "":
            return None
        else:
            return float(self.txt_nutrient_mass.text())

    @property
    def nutrient_mass_units(self) -> str:
        """Returns the units for the nutrient mass."""
        return self.cmb_nutrient_mass_unit.currentText()

    @property
    def ingredient_qty(self) -> typing.Optional[float]:
        """Returns the ingredient qty value."""
        if self.txt_ingredient_qty.text() == "":
            return None
        else:
            return float(self.txt_ingredient_qty.text())

    @property
    def ingredient_qty_units(self) -> str:
        """Returns the units for the ingredient quantity."""
        return self.cmb_ingredient_qty_unit.currentText()

    def set_nutrient_name(self, nutrient_name: str) -> None:
        """Sets the nutrient name on the widget."""
        self.lbl_nutrient_name.setText(f"{nutrient_name}:")

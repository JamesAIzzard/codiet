import typing

from PyQt6 import QtWidgets, uic

import app


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
        self.txt_nutrient_mass: app.CodietNumberLineEdit
        self.cmb_nutrient_mass_unit: app.CodietComboBox
        self.txt_ingredient_qty: app.CodietNumberLineEdit
        self.cmb_ingredient_qty_unit: app.CodietComboBox

        # Bring the ui file in
        uic.load_ui.loadUi("app/nutrient_ratio_editor.ui", self)

        # Add positive float validator to numerical input
        self.txt_ingredient_qty.setValidator(app.PositiveFloatValidator())
        self.txt_nutrient_mass.setValidator(app.PositiveFloatValidator())

        # Update the nutrient name label
        self.set_nutrient_name(nutrient_str)

        # Bind nutrient mass change handler if passed
        if on_nutrient_mass_change is not None:
            self.txt_nutrient_mass.textChanged.connect(on_nutrient_mass_change)

    @property
    def nutrient_ratio_defined(self) -> bool:
        """Returns True/False to indicate if the fields are populated."""
        if self.txt_nutrient_mass.text() is None or self.txt_ingredient_qty is None:
            return False
        else:
            return True

    def set_nutrient_name(self, nutrient_name: str) -> None:
        """Sets the nutrient name on the widget."""
        self.lbl_nutrient_name.setText(f"{nutrient_name}:")

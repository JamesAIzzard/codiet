from typing import Union

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QDoubleValidator


class NumericLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a QDoubleValidator object to validate the input as a double value.
        # The QDoubleValidator takes the following parameters:
        # - bottom (float): The minimum value allowed.
        # - top (float): The maximum value allowed.
        # - decimals (int): The number of decimal places allowed.
        validator = QDoubleValidator(0.0, 99999999.99, 2)
        self.setValidator(validator)

    def text(self) -> float | None:
        """Return the text of the line edit."""
        # Grab the text from super
        text = super().text()
        if text.strip() == "":
            return None
        else:
            return float(text)

    def setText(self, value: float | None, pad_decimals: int = 1) -> None:
        """Set the text of the line edit to the given value,
        formatted to the specified number of decimal places."""
        if value is None:
            super().setText("")
        else:
            formatted_value = f"{value:.{pad_decimals}f}"
            super().setText(formatted_value)

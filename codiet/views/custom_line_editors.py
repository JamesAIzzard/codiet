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

    @property
    def value(self) -> float | None:
        """Return the value of the line edit as a float.
        If the line edit is empty, return None."""
        if self.text() == "":
            return None
        return float(self.text())

    def setText(self, value: float, decimals: int = 1) -> None:
        """Set the text of the line edit to the given value,
        formatted to the specified number of decimal places."""
        formatted_value = f"{value:.{decimals}f}"
        super().setText(formatted_value)

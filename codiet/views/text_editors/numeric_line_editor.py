from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import pyqtSignal, QVariant

from codiet.views.text_editors.line_editor import LineEditor

class NumericLineEdit(LineEditor):
    """A QLineEdit widget that only accepts numeric input."""
    # Define the signals
    valueChanged = pyqtSignal(QVariant)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a QDoubleValidator object to validate the input as a double value.
        # The QDoubleValidator takes the following parameters:
        # - bottom (float): The minimum value allowed.
        # - top (float): The maximum value allowed.
        # - decimals (int): The number of decimal places allowed.
        validator = QDoubleValidator(0.0, 99999999.99, 2)
        self.setValidator(validator)

        # Connect the textChanged signal to the on_text_changed method.
        self.textChanged.connect(self.on_text_changed)

    def text(self) -> float | None:
        """Return the text of the line edit."""
        # Grab the text from super
        text = super().text()
        if text is None:
            return None
        else:
            return float(text)

    def setText(self, value: float | None, pad_decimals: int = 1) -> None:
        """Set the text of the line edit to the given value,
        formatted to the specified number of decimal places."""
        if value is None:
            super().clear()
        else:
            formatted_value = f"{value:.{pad_decimals}f}"
            super().setText(formatted_value)

    def on_text_changed(self, text: str) -> None:
        """Emit the valueChanged signal when the text changes."""
        if text.strip() == "":
            self.valueChanged.emit(None)
        else:
            self.valueChanged.emit(float(text))
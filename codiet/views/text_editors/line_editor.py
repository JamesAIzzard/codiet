from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import pyqtSignal, QVariant

class LineEditor(QLineEdit):
    """Extend the native QLineEdit class.
    Adds a lostFocus signal that emits the text of the line edit when it loses focus.
    Adds functionality to get and set None if the text is empty.
    """
    lostFocus = pyqtSignal(QVariant)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def text(self) -> str | None:
        """Return the text of the line edit."""
        text = super().text()
        if text.strip() == "":
            return None
        else:
            return text
        
    def setText(self, value: str | None) -> None:
        """Set the text of the line edit to the given value."""
        if value is None:
            super().clear()
        else:
            super().setText(str(value))

    def focusOutEvent(self, event):
        """Emit the lostFocus signal when the line edit loses focus."""
        self.lostFocus.emit(self.text())
        super().focusOutEvent(event)
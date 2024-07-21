from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import pyqtSignal, QVariant

class MultilineEditor(QTextEdit):
    """Extend the native QTextEdit class."""
    lostFocus = pyqtSignal(QVariant)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def text(self) -> str | None:
        """Return the text of the text edit."""
        text = super().toPlainText()
        if text.strip() == "":
            return None
        else:
            return text

    def setText(self, value: str | None) -> None:
        """Set the text of the text edit to the given value."""
        if value is None:
            super().clear()
        else:
            super().setText(str(value))

    def focusOutEvent(self, event):
        """Emit the lostFocus signal when the text edit loses focus."""
        self.lostFocus.emit(self.text())
        super().focusOutEvent(event)
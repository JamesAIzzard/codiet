from PyQt6.QtWidgets import (
    QWidget, 
    QLineEdit, 
    QHBoxLayout, 
    QPushButton
)
from PyQt6.QtCore import pyqtSignal


class SearchBoxView(QWidget):
    # Define singals
    cancelClicked = pyqtSignal()
    searchTermChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Build the UI
        self._build_ui()

        # Emit a signal when the cancel button is clicked
        self.btn_cancel.clicked.connect(self.cancelClicked.emit)
        # Emit a signal when the search box is edited.
        # The signal will pass the current text in the search box.
        # This is automatic because the signal is connected to the textChanged signal of the search box.
        self.txt_search.textChanged.connect(self.searchTermChanged.emit)

    @property
    def current_text(self) -> str:
        """Return the text in the search box."""
        return self.txt_search.text()
    
    def clear(self) -> None:
        """Clear the search box."""
        self.txt_search.clear()

    def _build_ui(self):
        """Build the user interface."""
        # Create a layout for the widget
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Create a search textbox and add it to the layout
        self.txt_search = QLineEdit()
        layout.addWidget(self.txt_search)

        # Create a cancel button and add it to the layout
        self.btn_cancel = QPushButton("X")

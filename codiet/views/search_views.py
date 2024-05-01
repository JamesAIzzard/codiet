from PyQt6.QtWidgets import (
    QWidget, 
    QLineEdit, 
    QHBoxLayout, 
    QPushButton,
    QVBoxLayout,
    QListWidget,
    QDialog,
    QSizePolicy
)
from PyQt6.QtCore import pyqtSignal


class SearchTermView(QWidget):
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
        layout.addWidget(self.btn_cancel)

class SearchPopupView(QDialog):
    """UI element to allow the user to search for ingredients."""
    # Define signals
    resultSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._build_ui()

        # Emit the signals
        self.lst_search_results.itemClicked.connect(self.resultSelected.emit)

    def update_results_list(self, matching_ingredient_names: list[str]):
        """Update the list of ingredients."""
        # Clear the existing ingredients
        self.lst_search_results.clear()
        # Add the matching ingredients
        for ingredient_name in matching_ingredient_names:
            self.lst_search_results.addItem(ingredient_name)

    def show(self):
        """Show the dialog."""
        self.exec()

    def _build_ui(self):
        """Build the user interface."""
        self.setWindowTitle("Ingredient Search")
        self.resize(400, 300)

        # Create a layout for the dialog
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a search textbox and add it to the layout
        self.search_term_textbox = SearchTermView()
        layout.addWidget(self.search_term_textbox)

        # Create a dropdown and add it to the layout
        self.lst_search_results = QListWidget()
        # Make the dropdown fill the space
        self.lst_search_results.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.lst_search_results)
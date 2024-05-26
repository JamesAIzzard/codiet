from PyQt6.QtWidgets import (
    QWidget, 
    QLineEdit, 
    QHBoxLayout, 
    QVBoxLayout,
    QListWidget,
    QSizePolicy
)
from PyQt6.QtCore import pyqtSignal

from codiet.utils.pyqt import block_signals
from codiet.views.buttons import ClearButton
from codiet.views.labels import SearchIconLabel

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
    
    @current_text.setter
    def current_text(self, text: str) -> None:
        """Set the text in the search box."""
        with block_signals(self.txt_search):
            self.txt_search.setText(text)
    
    def clear(self) -> None:
        """Clear the search box."""
        with block_signals(self.txt_search):
            self.txt_search.clear()

    def _build_ui(self):
        """Build the user interface."""
        # Create a layout for the widget
        layout = QHBoxLayout()
        # Reduce margins
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Add the search icon
        lbl_search_icon = SearchIconLabel()
        layout.addWidget(lbl_search_icon)

        # Create a search textbox and add it to the layout
        self.txt_search = QLineEdit()
        layout.addWidget(self.txt_search)
        # Make it occupy the maximum width
        layout.setStretchFactor(self.txt_search, 1)

        # Create a cancel button and add it to the layout
        self.btn_cancel = ClearButton()
        layout.addWidget(self.btn_cancel)

class SearchColumnView(QWidget):
    """UI element to allow the user to search and select a result."""
    # Define signals
    resultSelected = pyqtSignal(str)
    searchTermChanged = pyqtSignal(str)
    searchTermCleared = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._build_ui()

    @property
    def selected_result(self) -> str | None:
        """Return the selected result."""
        if self.result_is_selected:
            return self.lst_search_results.currentItem().text() # type: ignore
        else:
            return None

    @property
    def selected_index(self) -> int:
        """Return the index of the selected result."""
        return self.lst_search_results.currentRow()

    @property
    def result_is_selected(self) -> bool:
        """Return True if a result is selected."""
        return self.selected_index != -1

    def update_results_list(self, matching_results: list[str]):
        """Update the list of ingredients."""
        # Clear the existing ingredients
        self.lst_search_results.clear()
        # Add the matching ingredients
        for result in matching_results:
            self.lst_search_results.addItem(result)

    def clear_results_list(self):
        """Clear the search results."""
        self.lst_search_results.clear()

    def clear_search_term(self):
        """Clear the search term."""
        self.search_term_textbox.clear()

    def _on_result_selected(self, item):
        """Handle the user selecting a result to edit."""
        # Emit a signal with the selected text
        self.resultSelected.emit(item.text())

    def _build_ui(self):
        lyt_top_level = QVBoxLayout()
        lyt_top_level.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lyt_top_level)

        # Create a search textbox and add it to the layout
        self.search_term_textbox = SearchTermView()
        lyt_top_level.addWidget(self.search_term_textbox)
        # Connect the signals
        self.search_term_textbox.searchTermChanged.connect(self.searchTermChanged.emit)
        self.search_term_textbox.cancelClicked.connect(self.searchTermCleared.emit)
        # Create a dropdown and add it to the layout
        self.lst_search_results = QListWidget()
        # Connect the itemClicked signal to the _on_result_selected method
        self.lst_search_results.itemClicked.connect(self._on_result_selected)
        # Make the dropdown fill the space
        self.lst_search_results.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        lyt_top_level.addWidget(self.lst_search_results)
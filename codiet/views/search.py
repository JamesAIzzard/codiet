from PyQt6.QtWidgets import (
    QWidget, 
    QLineEdit, 
    QHBoxLayout, 
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QSizePolicy
)
from PyQt6.QtCore import pyqtSignal

from codiet.utils.pyqt import block_signals
from codiet.views.buttons import ClearButton
from codiet.views.labels import SearchIconLabel
from codiet.views.listbox import ListBox

class SearchTermView(QWidget):
    # Define singals
    clearSearchTermClicked = pyqtSignal()
    searchTermChanged = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Build the UI
        self._build_ui()

        # Emit a signal when the cancel button is clicked
        self.btn_clear.clicked.connect(self.clearSearchTermClicked.emit)
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
        self.btn_clear = ClearButton()
        layout.addWidget(self.btn_clear)

class SearchColumnView(QWidget):
    """UI element to allow the user to search and select a result."""
    # Define signals
    resultSelected = pyqtSignal(QListWidgetItem)
    searchTermChanged = pyqtSignal(str)
    searchTermCleared = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._build_ui()

    @property
    def results_list(self) -> ListBox:
        """Return the list of search results."""
        return self.lst_search_results

    def clear_search_term(self):
        """Clear the search term."""
        self.search_term_textbox.clear()

    def _build_ui(self):
        lyt_top_level = QVBoxLayout()
        lyt_top_level.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lyt_top_level)

        # Create a search textbox and add it to the layout
        self.search_term_textbox = SearchTermView()
        lyt_top_level.addWidget(self.search_term_textbox)
        # Connect the signals
        self.search_term_textbox.searchTermChanged.connect(self.searchTermChanged.emit)
        self.search_term_textbox.clearSearchTermClicked.connect(self.searchTermCleared.emit)
        # Create a dropdown and add it to the layout
        self.lst_search_results = ListBox(parent=self)
        # Connect the itemClicked signal to the _on_result_selected method
        self.lst_search_results.itemClicked.connect(self.resultSelected.emit)
        # Make the dropdown fill the space
        self.lst_search_results.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        lyt_top_level.addWidget(self.lst_search_results)
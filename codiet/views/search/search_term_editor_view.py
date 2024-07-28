from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal

from codiet.views import block_signals
from codiet.views.labels import SearchIconLabel
from codiet.views.icon_button import IconButton
from codiet.views.text_editors.line_editor import LineEditor

class SearchTermEditorView(QWidget):
    """A search term view that contains a search box and a clear button.

    Signals:
        clearSearchTermClicked: Emitted when the clear button is clicked.
            No arguments.
        searchTermChanged: Emitted when the search term is changed
            Has a single argument, the new search term (str).
    """

    clearSearchTermClicked = pyqtSignal()
    searchTermChanged = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Build the UI
        self._build_ui()

        # Connect signals and slots
        self.btn_clear.clicked.connect(self.clearSearchTermClicked.emit)
        self.txt_search.textChanged.connect(self.searchTermChanged.emit)

    @property
    def current_text(self) -> str|None:
        """Return the text in the search box."""
        return self.txt_search.text()
    
    @current_text.setter
    def current_text(self, text: str|None) -> None:
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
        self.txt_search = LineEditor()
        layout.addWidget(self.txt_search)
        # Make it occupy the maximum width
        layout.setStretchFactor(self.txt_search, 1)

        # Create a cancel button and add it to the layout
        self.btn_clear = IconButton(icon_filename="cancel-icon.png")
        layout.addWidget(self.btn_clear)
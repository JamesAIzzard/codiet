from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject, pyqtSignal

from codiet.views.search.searchbox_view import SearchboxView

class Searchbox(QObject):
    """Searchbox module for searching and selecting a result.
    
    Signals:
        searchTermChanged: Emitted when the search term is changed.
            Has a single argument, the new search term (str).
        clearSearchTermClicked: Emitted when the clear button is clicked.
            No arguments.
    """
    searchTermChanged = pyqtSignal(str)
    clearSearchTermClicked = pyqtSignal()

    def __init__(
            self,
            view: SearchboxView|None=None,
            parent: QWidget|None=None
    ):
        # Stash the view
        if view is None:
            self.view = SearchboxView(
                parent=parent or None
            )
        else:
            self.view = view
        # Connect signals
        self.view.searchTermChanged.connect(self.searchTermChanged.emit)
        self.view.clearSearchTermClicked.connect(self.clearSearchTermClicked.emit)
        
    @property
    def current_text(self) -> str:
        """Return the current text in the search box."""
        return self.view.current_text
    
    @current_text.setter
    def current_text(self, text: str) -> None:
        """Set the text in the search box."""
        self.view.current_text = text

    def clear(self) -> None:
        """Clear the search box."""
        self.view.clear()
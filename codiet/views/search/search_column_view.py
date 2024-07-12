from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidgetItem,
    QSizePolicy
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt

from codiet.views.listbox import ListBox
from codiet.views.search.searchbox_view import SearchboxView

class SearchColumnView(QWidget):
    """UI element to allow the user to search and select a result."""
    # Define signals
    resultClicked = pyqtSignal(object, object) # list widget content, data
    searchTermChanged = pyqtSignal(str)
    searchTermCleared = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_ui()
        # Connect signals and slots
        self.lst_search_results.itemClicked.connect(self._on_item_clicked)
        self.searchbox_view.searchTermChanged.connect(self.searchTermChanged.emit)
        self.searchbox_view.clearSearchTermClicked.connect(self.searchTermCleared.emit)

    def _on_item_clicked(self, item: QListWidgetItem):
        # Determine if the item contains a widget or just text
        widget = self.lst_search_results.itemWidget(item)
        if widget:
            item_content = widget
        else:
            item_content = item.text()
        
        # Emit the resultClicked signal with the item's content and data
        self.resultClicked.emit(item_content, item.data(Qt.ItemDataRole.UserRole))

    def _build_ui(self):
        lyt_top_level = QVBoxLayout()
        lyt_top_level.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lyt_top_level)

        # Create a search textbox and add it to the layout
        self.searchbox_view = SearchboxView(parent=self)
        lyt_top_level.addWidget(self.searchbox_view)
        # Create a dropdown and add it to the layout
        self.lst_search_results = ListBox(parent=self)
        # Make the dropdown fill the space
        self.lst_search_results.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        lyt_top_level.addWidget(self.lst_search_results)
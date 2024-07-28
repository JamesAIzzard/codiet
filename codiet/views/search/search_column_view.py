from PyQt6.QtWidgets import (
    QWidget,
    QListWidget,
    QVBoxLayout,
    QSizePolicy
)

from codiet.views.search.search_term_editor_view import SearchTermEditorView

class SearchColumnView(QWidget):
    """UI element to allow the user to search and select a result."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._build_ui()

    def _build_ui(self):
        lyt_top_level = QVBoxLayout()
        lyt_top_level.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lyt_top_level)

        # Create a search textbox and add it to the layout
        self.search_term_editor_view = SearchTermEditorView(parent=self)
        lyt_top_level.addWidget(self.search_term_editor_view)
        # Create a dropdown and add it to the layout
        self.results_list_view = QListWidget(parent=self)
        # Make the dropdown fill the space
        self.results_list_view.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        lyt_top_level.addWidget(self.results_list_view)
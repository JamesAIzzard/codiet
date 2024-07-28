from codiet.views.search.search_term_editor_view import SearchTermEditorView
from codiet.controllers.base_controller import BaseController

class SearchTermEditor(BaseController[SearchTermEditorView]):
    """A search term editor module, including a label, textbox and clear button."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Connect signals and slots
        self.view.clearSearchTermClicked.connect(self._on_clear_clicked)

    def _on_clear_clicked(self) -> None:
        """Clears the textbox when clear is clicked."""
        self.view.clear()

    def _create_view(self, *args, **kwargs) -> SearchTermEditorView:
        return SearchTermEditorView(*args, **kwargs)
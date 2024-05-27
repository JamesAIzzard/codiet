from typing import Callable

from codiet.utils.search import filter_text
from codiet.views.search_views import SearchColumnView

class SearchColumnCtrl:
    def __init__(
            self, 
            view: SearchColumnView, 
            get_data: Callable[[], list[str]],
            on_result_selected: Callable[[str], None]
        ) -> None:
        self.view = view
        self.get_data = get_data
        self.on_result_selected = on_result_selected
        self._connect_signals()
        self.view.update_results_list(self.get_data())

    def _on_search_term_changed(self, search_term: str) -> None:
        """Handler for changes to the search column."""
        # Clear the search UI
        self.view.clear_results_list()
        # If the search term is empty
        if search_term.strip() == "":
            # Populate the list with all ingredient names
            self.view.update_results_list(self.get_data())
        else:
            # Find the 10x best matches
            best_matches = filter_text(search_term, self.get_data(), 10)
            # Add the best matches to the search column
            self.view.update_results_list(best_matches)

    def _on_search_term_cleared(self) -> None:
        """Handler for clearing the search term."""
        # Clear the search column
        self.view.clear_results_list()
        # Clear the search term
        self.view.clear_search_term()
        # Populate the list with all ingredient names
        self.view.update_results_list(self.get_data())

    def _connect_signals(self) -> None:
        """Connect the signals and slots to the search column."""
        self.view.searchTermChanged.connect(self._on_search_term_changed)
        self.view.searchTermCleared.connect(self._on_search_term_cleared)
        self.view.resultSelected.connect(
            lambda: self.on_result_selected(self.view.selected_result) # type: ignore
        )
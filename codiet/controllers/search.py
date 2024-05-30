from typing import Callable

from PyQt6.QtWidgets import (
    QListWidgetItem
)

from codiet.utils.search import filter_text
from codiet.views.search import SearchColumnView

class SearchColumnCtrl():
    def __init__(
            self, 
            view: SearchColumnView, 
            get_searchable_strings: Callable[[], list[str]],
            on_result_selected: Callable[[QListWidgetItem], None],
            get_result_for_string: Callable[[str], QListWidgetItem]|None=None,
            num_matches: int = 10
        ) -> None:
        self.view = view
        self.get_searchable_strings = get_searchable_strings
        self.on_result_selected = on_result_selected
        self.num_matches = num_matches
        if get_result_for_string is None:
            self.get_result_for_string = lambda result: QListWidgetItem(result)
        # Connect the view up
        self.view.searchTermChanged.connect(self._on_search_term_changed)
        self.view.searchTermCleared.connect(self._on_search_term_cleared)
        self.view.resultSelected.connect(
            lambda: self.on_result_selected(self.view.selected_result) # type: ignore
        )
        # Initially populate the list
        self.show_all_items()

    def show_all_items(self) -> None:
        """Show all items in the search column."""
        # Get a list of items for all the searchable strings
        items = self._get_items_for_results(self.get_searchable_strings())
        self.view.update_results_list(items)

    def _get_items_for_results(self, results: list[str]) -> list[QListWidgetItem]:
        """Create QListWidgetItems for the results."""
        items = []
        for result in results:
            item = self.get_result_for_string(result)
            items.append(item)
        return items

    def _on_search_term_changed(self, search_term: str) -> None:
        """Handler for changes to the search column."""
        # Clear the search UI
        self.view.clear_results_list()
        # If the search term is empty
        if search_term.strip() == "":
            self.show_all_items()
        else:
            # Find the 10x best matches
            best_matches = filter_text(
                search_term, 
                self.get_searchable_strings(), 
                self.num_matches
            )
            # For each best match, get the corresponding list item
            best_match_items = self._get_items_for_results(best_matches)
            # Add the best matches to the search column
            self.view.update_results_list(best_match_items)

    def _on_search_term_cleared(self) -> None:
        """Handler for clearing the search term."""
        # Clear the search column
        self.view.clear_results_list()
        # Clear the search term
        self.view.clear_search_term()
        # Populate the list with all ingredient names
        self.show_all_items()

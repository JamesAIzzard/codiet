from typing import Callable, Any

from PyQt6.QtWidgets import (
    QWidget,
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
            get_view_item_and_data_for_string: Callable[[str], (QWidget|str, Any)]|None=None,
            num_matches: int = 10
        ) -> None:
        self.view = view
        self.get_searchable_strings = get_searchable_strings
        self.on_result_selected = on_result_selected
        self.num_matches = num_matches
        # If there was no widget fetching function provided, just
        # return the string
        if get_view_item_and_data_for_string is None:
            self.get_result_for_string = lambda result: result
        else:
            self.get_result_for_string = get_view_item_and_data_for_string
        # Connect the view up
        self.view.searchTermChanged.connect(self._on_search_term_changed)
        self.view.searchTermCleared.connect(self._on_search_term_cleared)
        self.view.resultClicked.connect(
            lambda: self.on_result_selected(self.view.results_list.selected_item) # type: ignore
        )
        # Initially populate the list
        self.show_all_items()

    def show_all_items(self) -> None:
        """Show all items in the search column."""
        # Get a list of items for all the searchable strings
        items = self._get_view_items_for_results(self.get_searchable_strings())
        self.view.results_list.update_list(items)

    def reset_search(self) -> None:
        """Reset the search column.
        Clears all search results and the search term, and
        repopulates the list with all items.
        """
        self.view.clear_search_term()
        self.show_all_items()

    def _get_view_items_for_results(self, results: list[str]) -> list[QWidget|str]:
        """Convert the result strings into a list of widgets if
        a conversion function was required. Otherwise just return
        the strings."""
        items = []
        for result in results:
            item = self.get_result_for_string(result)
            items.append(item)
        return items

    def _on_search_term_changed(self, search_term: str) -> None:
        """Handler for changes to the search column."""
        # Clear the search UI
        self.view.results_list.clear_list()
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
            best_match_items = self._get_view_items_for_results(best_matches)
            # Add the best matches to the search column
            self.view.results_list.update_list(best_match_items)

    def _on_search_term_cleared(self) -> None:
        """Handler for clearing the search term."""
        # Clear the search column
        self.view.results_list.clear_list()
        # Clear the search term
        self.view.clear_search_term()
        # Populate the list with all ingredient names
        self.show_all_items()

from typing import Tuple, Callable, Any

from PyQt6.QtWidgets import (
    QWidget
)

from codiet.utils.search import filter_text
from codiet.views.search import SearchColumnView

class SearchColumnCtrl():
    def __init__(
            self, 
            view: SearchColumnView, 
            get_searchable_strings: Callable[[], list[str]],
            on_result_selected: Callable[[Tuple[QWidget|str, Any]], None],
            get_view_item_and_data_for_string: Callable[[str], Tuple[QWidget|str, Any]]|None=None,
            num_matches: int = 10
        ) -> None:
        """Initialise the SearchColumnCtrl object. 
        Args:
            view (SearchColumnView): The view object.
            get_searchable_strings (Callable[[], list[str]]): A function that returns a list of strings to search.
            on_result_selected (Callable[[QWidget|str], None]): The function to call when a result is selected.
                The arguments are the view item or string that was selected, and the associated data.
            get_view_item_and_data_for_string (Callable[[str], Tuple[QWidget|str, Any]], optional): A function that returns a view item and associated data for a given string. Defaults to None.
            num_matches (int, optional): The number of best matches to find. Defaults to 10.
        """
        self.view = view
        self.get_searchable_strings = get_searchable_strings
        self.on_result_selected = on_result_selected
        self.num_matches = num_matches
        # If there was no widget fetching function provided, just
        # return the string
        if get_view_item_and_data_for_string is None:
            self.get_view_item_and_data_for_string = lambda text: text
        else:
            self.get_view_item_and_data_for_string = get_view_item_and_data_for_string
        # Connect the view up
        self.view.searchTermChanged.connect(self._on_search_term_changed)
        self.view.searchTermCleared.connect(self._on_search_term_cleared)
        self.view.resultClicked.connect(
            lambda item: self.on_result_selected(item)
        )
        # Initially populate the list
        self.show_all_items()

    def show_all_items(self) -> None:
        """Show every possible result in the results list, without filtering."""
        # Get a list of items for all the searchable strings
        items_and_data = self._get_view_items_and_data_for_results(self.get_searchable_strings())
        self.view.lst_search_results.update_list(items_and_data)

    def reset_search(self) -> None:
        """Reset the search column.
        Clears all search results and the search term, and
        repopulates the list with all items.
        """
        self.view.search_term_textbox.clear()
        self.show_all_items()

    def _get_view_items_and_data_for_results(self, results: list[str]) -> list[tuple[QWidget|str, Any]]:
        """Convert a list of strings (filtered by the search term) into their corresponding
        view items and associated data.
        Args:
            results (list[str]): The list of strings to convert.
        Returns:
            list[tuple[QWidget|str, Any]]: The list of view items and data.
        """
        items_and_data = []
        for result in results:
            item_and_data = self.get_view_item_and_data_for_string(result)
            items_and_data.append(item_and_data)
        return items_and_data

    def _on_search_term_changed(self, search_term: str) -> None:
        """Handler for changes to the search column."""
        # Clear the search UI
        self.view.search_term_textbox.clear()
        # If the search term is empty
        if search_term.strip() == "":
            self.show_all_items()
        else:
            # Find the specified number of best matches
            best_matches = filter_text(
                search_term, 
                self.get_searchable_strings(), 
                self.num_matches
            )
            # For each best match, get the corresponding list item
            best_match_items_and_data = self._get_view_items_and_data_for_results(best_matches)
            # Add the best matches to the search column
            self.view.lst_search_results.update_list(best_match_items_and_data)

    def _on_search_term_cleared(self) -> None:
        """Handler for clearing the search term."""
        # Clear the search column
        self.view.lst_search_results.clear()
        # Clear the search term
        self.view.search_term_textbox.clear()
        # Populate the list with all ingredient names
        self.show_all_items()

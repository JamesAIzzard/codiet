from typing import Tuple, Callable, Any

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget
)

from codiet.utils.search import filter_text
from codiet.views.search.search_column_view import SearchColumnView
from codiet.controllers.search.searchbox import Searchbox

class SearchColumn(QObject):
    """A search column module, with a search textbox and results list.
    Essentially this is a module which presents the user with a list of items,
    and raises an event when the user clicks on one of them.

    Signals:
        onResultSelected: Emitted when a result is selected.
            Has two arguments: the view item or string that was selected, and the associated data.
    """

    onResultSelected = pyqtSignal(object, object)

    def __init__(
            self, 
            get_searchable_strings: Callable[[], list[str]],
            get_view_item_and_data_for_string: Callable[[str], Tuple[QWidget|str, Any]]|None=None,
            num_matches: int = 10,
            view: SearchColumnView|None=None,
            parent: QWidget|None=None
        ) -> None:
        """Initialise the SearchColumnCtrl object. 
        Args:
            get_searchable_strings (Callable[[], list[str]]): A function that returns a list of strings to search.
            get_view_item_and_data_for_string (Callable[[str], Tuple[QWidget|str, Any]], optional): A function that returns a view item and associated data for a given string. Defaults to None.
            num_matches (int, optional): The number of best matches to find. Defaults to 10.
            view (SearchColumnView): The view object. Defaults to None.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        
        # Instantiate the view if not submitted
        if view is None:
            self.view = SearchColumnView(
                parent=parent or None
            )
        else:
            self.view = view

        # Stash constructor parameters
        self._get_searchable_strings = get_searchable_strings
        self._num_matches = num_matches
        # If there was no widget fetching function provided, just
        # return the string
        if get_view_item_and_data_for_string is None:
            self.get_view_item_and_data_for_string = lambda text: text
        else:
            self.get_view_item_and_data_for_string = get_view_item_and_data_for_string
            
        # Init the search textbox module
        self.searchbox = Searchbox(
            parent=self.view,
            view=self.view.searchbox_view
        )

        # Connect the view up
        self.view.searchTermChanged.connect(self._on_search_term_changed)
        self.view.searchTermCleared.connect(self._on_search_term_cleared)
        self.view.resultClicked.connect(self._on_result_clicked)
        # Initially populate the list
        self.show_all_items()

    def show_all_items(self) -> None:
        """Show every possible result in the results list, without filtering."""
        # Get a list of items for all the searchable strings
        items_and_data = self._get_view_items_and_data_for_results(self._get_searchable_strings())
        self.view.search_results.update_list(items_and_data)

    def reset_search(self) -> None:
        """Reset the search column.
        Clears all search results and the search term, and
        repopulates the list with all items.
        """
        self.view.searchbox_view.clear()
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

    def _on_result_clicked(self, item_content: QWidget|str, data: Any) -> None:
        """Handler for when a result is clicked."""
        self.onResultSelected.emit(item_content, data)

    def _on_search_term_changed(self, search_term: str) -> None:
        """Handler for changes to the search column."""
        # Clear the search UI
        self.view.searchbox_view.clear()
        # If the search term is empty
        if search_term.strip() == "":
            self.show_all_items()
        else:
            # Find the specified number of best matches
            best_matches = filter_text(
                search_term, 
                self._get_searchable_strings(), 
                self._num_matches
            )
            # For each best match, get the corresponding list item
            best_match_items_and_data = self._get_view_items_and_data_for_results(best_matches)
            # Add the best matches to the search column
            self.view.search_results.update_list(best_match_items_and_data)

    def _on_search_term_cleared(self) -> None:
        """Handler for clearing the search term."""
        # Clear the search column
        self.view.search_results.clear()
        # Clear the search term
        self.view.searchbox_view.clear()
        # Populate the list with all ingredient names
        self.show_all_items()

from typing import TypeVar, Generic, Tuple, Callable, Any

from PyQt6.QtWidgets import QWidget

from codiet.utils.search import filter_text
from codiet.views.search.search_column_view import SearchColumnView
from codiet.controllers.base_controller import BaseController
from codiet.controllers.search.search_term_editor import SearchTermEditor
from codiet.controllers.listbox import Listbox

T = TypeVar('T')  # Object associated with each result view
V = TypeVar('V', bound=QWidget)  # Type of result view

class SearchColumn(BaseController[SearchColumnView], Generic[T, V]):
    """A search column module, with a search textbox and results list.
    Essentially this is a module which presents the user with a list of items,
    and raises an event when the user clicks on one of them.
    """

    def __init__(
            self, 
            get_searchable_strings: Callable[[], list[str]],
            get_item_and_view_for_string: Callable[[str], Tuple[T, V]],
            num_matches: int = 10,
            *args, **kwargs
        ) -> None:
        """Initialise the SearchColumn object. 
        Args:
            get_searchable_strings (Callable[[], list[str]]): A function that returns a list of strings to search.
            get_view_item_and_data_for_string (Callable[[str], Tuple[T, V]]): A function that returns the item and view associated with a string.
            num_matches (int, optional): The number of best matches to find. Defaults to 10.
        """
        super().__init__(*args, **kwargs)

        self._get_searchable_strings = get_searchable_strings
        self._num_matches = num_matches
        self.get_view_item_and_data_for_string = get_item_and_view_for_string
            
        self.search_term_editor = SearchTermEditor(view=self.view.search_term_editor_view)
        self.results_list = Listbox[T, V](view=self.view.results_list_view)

        self.search_term_editor.view.clearSearchTermClicked.connect(self.reset_search)

        # Initially reset the search column
        self.reset_search()

    def show_all_items(self) -> None:
        """Show every possible result in the results list, without filtering."""
        # Get a list of all searchable strings
        all_strings = self._get_searchable_strings()
        # Convert these into view items and data
        items_and_data = self._get_items_and_views_for_strings(all_strings)
        # Add these to the search column.
        self.results_list.add_rows(items_and_views=items_and_data)

    def reset_search(self) -> None:
        """Reset the search column.
        Clears all search results and the search term, and
        repopulates the list with all items.
        """
        self.view.search_term_editor_view.clear()
        self.results_list.clear()
        self.show_all_items()

    def _create_view(self, *args, **kwargs) -> SearchColumnView:
        return SearchColumnView(*args, **kwargs)

    def _get_items_and_views_for_strings(self, strings: list[str]) -> list[tuple[T, V]]:
        """Convert a list of strings (filtered by the search term) into their corresponding
        view items and associated data.
        Args:
            results (list[str]): The list of strings to convert.
        Returns:
            list[tuple[T, V]]: A list of tuples, where each tuple contains a view item and its associated
        """
        # Init the list to return
        items_and_views = []
        # For each string in the list
        for string in strings:
            # Create the item and the view
            item_and_view = self.get_view_item_and_data_for_string(string)
            items_and_views.append(item_and_view)
        return items_and_views

    def _on_search_term_changed(self, search_term: str) -> None:
        """Handler for changes to the search column."""
        # Clear the results list
        self.results_list.clear()
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
            best_match_items_and_data = self._get_items_and_views_for_strings(best_matches)
            # Add the best matches to the search column
            self.results_list.add_rows(items_and_views=best_match_items_and_data)

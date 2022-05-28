import typing

from PyQt6 import QtWidgets, QtCore, uic
import PyQt6


class SearchWidgetView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load in the ui file
        uic.load_ui.loadUi("example_app/gui/flag_selector.ui", self)

        # Identify active widgets for controller
        self.lst_search_results: QtWidgets.QListWidget
        self.btn_search: QtWidgets.QPushButton
        self.chk_option: QtWidgets.QCheckBox
        self.txt_search_term: QtWidgets.QLineEdit
        self.btn_delete_selection: QtWidgets.QPushButton
        self.btn_edit_selection: QtWidgets.QPushButton

        # Live dict of results shown
        self._search_results: typing.List[str] = []

    @property
    def search_term(self) -> typing.Optional[str]:
        """Returns the current search term, or None if unpopulated."""
        if self.txt_search_term.text() == "":
            return None
        else:
            return self.txt_search_term.text()

    @property
    def search_results(self) -> typing.List[str]:
        """Returns a list of the currently dispayed strings."""
        return self._search_results.copy()

    def add_search_result(self, text: str) -> None:
        """Adds a search result to the results box."""
        if text not in self._search_results:
            self.lst_search_results.addItem(text)

    def remove_search_result(self, text: str) -> None:
        """Removes a specific search result from the list."""
        self.lst_search_results.takeItem(
            self.lst_search_results.row(
                self.lst_search_results.findItems(
                    text, QtCore.Qt.MatchFlag.MatchExactly
                )[0]
            )
        )

    def clear_search_results(self) -> None:
        """Clears all search results from the list."""
        self.lst_search_results.clear()

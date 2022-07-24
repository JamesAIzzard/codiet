import typing

from PyQt6 import QtWidgets, QtCore, uic


class SearchWidgetView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load in the ui file
        uic.load_ui.loadUi("app/search_widget.ui", self)

        # Identify active widgets for controller
        self.lst_search_results: QtWidgets.QListWidget
        self.btn_search: QtWidgets.QPushButton
        self.txt_search_term: QtWidgets.QLineEdit
        self.btn_delete_selection: QtWidgets.QPushButton
        self.btn_edit_selection: QtWidgets.QPushButton
        self.gp_search_widget: QtWidgets.QGroupBox

        # Live dict of results shown
        self._search_results: typing.List[str] = []

    @property
    def search_results(self) -> typing.List[str]:
        """Returns a list of the currently dispayed strings."""
        return self._search_results.copy()

    def set_title(self, title:str) -> None:
        """Sets the title of the widget."""
        self.gp_search_widget.setTitle(title)

    def add_search_result(self, result: str) -> None:
        """Adds a string to the results box."""
        if result not in self._search_results:
            self.lst_search_results.addItem(result)

    def add_search_results(self, results: typing.List[str]) -> None:
        """Adds a list of strings to the result box.
        - Does not add an item if it is already there.
        """
        for result in results:
            self.add_search_result(result)

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

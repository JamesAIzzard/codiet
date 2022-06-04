import typing

from PyQt6 import QtCore
from PyQt6.QtWidgets import QComboBox

class CodietComboBox(QComboBox):
    """Adds useful functionality to standard combobox."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_items_once(self, items:typing.List[str]) -> None:
        """Ensures each item on the list is present once and only once."""
        for item in items:
            if self.findText(item, flags=QtCore.Qt.MatchFlag.MatchExactly) is -1:
                self.addItem(item)        

    def remove_items(self, items: typing.List[str]) -> None:
        """Ensures that all items in the list are removed from the combobox."""
        for item in items:
            index = self.findText(item, flags=QtCore.Qt.MatchFlag.MatchExactly)
            if index is not -1:
                self.removeItem(index)

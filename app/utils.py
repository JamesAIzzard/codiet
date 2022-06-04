import typing

from PyQt6 import QtWidgets, QtCore

def cmb_add_items_once(combobox:QtWidgets.QComboBox, items: typing.List[str]) -> None:
    """Ensures each item in the list is present on the combo box
    once an only once."""
    for item in items:
        if combobox.findText(item, flags=QtCore.Qt.MatchFlag.MatchExactly) is -1:
            combobox.addItem(item)

def cmb_remove_items(combobox: QtWidgets.QComboBox, items: typing.List[str]) -> None:
    """Ensures that all items in the list are removed from the combobox."""
    for item in items:
        index = combobox.findText(item, flags=QtCore.Qt.MatchFlag.MatchExactly)
        if index is not -1:
            combobox.removeItem(index)
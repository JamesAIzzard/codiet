from math import comb
import typing

from PyQt6 import QtWidgets, QtCore

def cmb_add_items_once(combobox:QtWidgets.QComboBox, items: typing.List[str]) -> None:
    """Ensures each item in the list is present on the combo box
    once an only once."""
    for item in items:
        if combobox.findText(item, flags=QtCore.Qt.MatchFlag.MatchExactly) is -1:
            combobox.addItem(item)
from typing import List, Optional

from PyQt6 import QtWidgets, uic

class FlagSelectorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load in the ui file
        uic.load_ui.loadUi('gui/flag_selector.ui', self)

        # Identify active widgets for controller
        self.btn_adopt_flag:QtWidgets.QPushButton
        self.btn_remove_flag: QtWidgets.QPushButton

    @property
    def selected_adopted_flag(self) -> Optional[str]:
        """Returns the currently selected adopted flag."""
        if self.lst_adopted_flags.currentItem() is not None: # type: ignore
            return self.lst_adopted_flags.currentItem().text() # type: ignore
        else:
            return None

    @property
    def all_adopted_flags(self) -> List[str]:
        """Returns a list of all the currently adopted flags in the widget's list."""
        flags: List[str] = []
        for i in range(0, self.lst_adopted_flags.count()): # type: ignore
            flags.append(self.lst_adopted_flags.item(i).text()) #type: ignore
        return flags

    @property
    def selected_global_flag(self) -> Optional[str]:
        """Returns the currently selected global flag."""
        if self.lst_global_flags.currentItem() is not None: # type: ignore
            return self.lst_global_flags.currentItem().text() # type: ignore
        else:
            return None

    def _add_flags(self, lst_widget:QtWidgets.QListWidget, flags) -> None:
        """Sets the flags on the widget provided."""
        # Now iterate through flags, setting them
        for flag in flags:
            lst_widget.addItem(flag)

    def set_adopted_flags(self, flags:List[str]) -> None:
        """Sets the flags in the adopted list."""
        self.clear_adopted_flags() # type: ignore
        self._add_flags(self.lst_adopted_flags, flags) # type: ignore

    def adopt_flag(self, flag:str) -> None:
        """Adds the flag to the adopted box, if not already there."""
        if flag not in self.all_adopted_flags:
            self.lst_adopted_flags.addItem(flag) # type: ignore

    def remove_flag(self, flag:str) -> None:
        """Removes the currently selected adopted flag from the adopted list."""
        for i in range(0, self.lst_adopted_flags.count()): # type: ignore
            if flag == self.lst_adopted_flags.item(i).text(): # type: ignore
                self.lst_adopted_flags.takeItem(i) # type: ignore
                break

    def clear_adopted_flags(self) -> None:
        """Clears the flags in the adopted list."""
        self.lst_adopted_flags.clear() # type: ignore

    def set_global_flags(self, flags: List[str]) -> None:
        """Sets the flags in the global list."""
        self.clear_global_flags()
        self._add_flags(self.lst_global_flags, flags) # type: ignore

    def clear_global_flags(self) -> None:
        """Clears the flags in the global list."""
        self.lst_global_flags.clear() # type: ignore
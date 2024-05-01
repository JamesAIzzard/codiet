from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal

from codiet.utils.pyqt import block_signals

class FlagEditorView(QWidget):
    """The UI element to allow the user to edit flags."""

    # Define signals
    onFlagChanged = pyqtSignal(str, bool)
    onSelectAllFlagsClicked = pyqtSignal()
    onDeselectAllFlagsClicked = pyqtSignal()
    onInvertSelectionFlagsClicked = pyqtSignal()
    onClearSelectionFlagsClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Build the UI
        self._build_ui()

        # Create a dict of the flag ui elements
        self.flags = {}

    def add_flag_to_list(self, flag_name) -> None:
        """Adds a flag to the list of checkable flags"""
        # Create the item
        item = QListWidgetItem(flag_name)
        # Make the item checkable
        item.setFlags(
            item.flags() | Qt.ItemFlag.ItemIsUserCheckable
        )
        # Set the item as initially unchecked
        item.setCheckState(Qt.CheckState.Unchecked)
        # Add the item to the UI
        self.lstFlagCheckboxes.addItem(item)
        # Add the item to the list in lowercase
        self.flags[flag_name.lower()] = item

    def set_flag(self, flag: str, value: bool) -> None:
        """Set the value of a flag."""
        # Update the flag in the UI
        if value is True:
            self.flags[flag].setCheckState(Qt.CheckState.Checked)
        else:
            self.flags[flag].setCheckState(Qt.CheckState.Unchecked)

    def update_flags(self, flags: dict[str, bool]) -> None:
        """Update the flags in the UI."""
        for flag_name, flag_value in flags.items(): # Don't need to block, set_flag blocks.
            self.set_flag(flag_name, flag_value)

    def select_all_flags(self):
        '''Select all flags.'''
        for flag in self.flags: # Don't need to block, set_flag blocks.
            self.set_flag(flag, True) 

    def deselect_all_flags(self):
        '''Deselect all flags.'''
        for flag in self.flags: # Don't need to block, set_flag blocks.
            self.set_flag(flag, False)
    
    def get_selected_flags(self) -> list[str]:
        '''Get a list of all the selected flags.'''
        selected_flags = []
        for flag in self.flags:
            if self.flags[flag].checkState() == Qt.CheckState.Checked:
                selected_flags.append(flag)
        return selected_flags
    
    def get_flag_value(self, flag: str) -> bool:
        '''Get the value of a flag.'''
        return self.flags[flag].checkState() == Qt.CheckState.Checked

    def _build_ui(self):
        """Build the UI for the flag editor"""
        # Create a vertical layout for the widget
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Reduce the vertical padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)        

        # Put a group box inside the vertical layout
        outer_group_box = QGroupBox("Flags")
        layout.addWidget(outer_group_box)

        # Create two columns, the LHS for a checkable list
        # and the RHS for the helper tools on buttons
        columns_layout = QHBoxLayout()
        outer_group_box.setLayout(columns_layout)

        # Add a listbox of checkable items to the LHS column
        self.lstFlagCheckboxes = QListWidget()

        # Reduce padding at the top of the group box
        columns_layout.setContentsMargins(5, 5, 5, 5)
        columns_layout.addWidget(self.lstFlagCheckboxes, 1)

        # Create a vertical list of buttons in the RHS column
        buttons_layout = QVBoxLayout()
        columns_layout.addLayout(buttons_layout, 0)

        # Populate buttons column with helper buttons
        # Add a 'Select All' button
        self.btn_select_all = QPushButton("Select All")
        buttons_layout.addWidget(self.btn_select_all)
        # Add a 'Deselect All' button
        self.btn_deselect_all = QPushButton("Deselect All")
        buttons_layout.addWidget(self.btn_deselect_all)
        # Add an 'Invert Selection' button
        self.btn_invert_selection = QPushButton("Invert Selection")
        buttons_layout.addWidget(self.btn_invert_selection)
        # Add a 'Clear Selection' button
        self.btn_clear_selection = QPushButton("Clear Selection")
        buttons_layout.addWidget(self.btn_clear_selection)
        # Push the buttons to the top
        buttons_layout.addStretch()
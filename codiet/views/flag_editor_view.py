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
        # If the flag is already in the list, raise an exception
        if flag_name.lower() in self.flags:
            raise ValueError(f"Flag '{flag_name}' is already in the list.")
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

    def add_flags_to_list(self, flags: list[str]) -> None:
        """Add a list of flags to the list of checkable flags"""
        for flag in flags:
            self.add_flag_to_list(flag)

    def remove_all_flags_from_list(self) -> None:
        """Remove all flags from the list of checkable flags"""
        self.lstFlagCheckboxes.clear()
        self.flags.clear()

    def update_flag(self, flag: str, value: bool) -> None:
        """Set the value of a flag."""
        # Update the flag in the UI
        # Block the signals to prevent the onFlagChanged signal from being emitted
        with block_signals(self.lstFlagCheckboxes):
            if value is True:
                self.flags[flag].setCheckState(Qt.CheckState.Checked)
            else:
                self.flags[flag].setCheckState(Qt.CheckState.Unchecked)

    def update_flags(self, flags: dict[str, bool]) -> None:
        """Update the flags in the UI."""
        for flag_name, flag_value in flags.items(): 
           self.update_flag(flag_name, flag_value)

    def set_all_flags_true(self):
        """Select all flags."""
        for flag in self.flags:
            self.update_flag(flag, True) 

    def set_all_flags_false(self):
        """Deselect all flags."""
        for flag in self.flags:
            self.update_flag(flag, False)
    
    def invert_flags(self):
        """Invert the selection of all flags."""
        for flag in self.flags:
            self.update_flag(flag, not self.get_flag_value(flag))

    def get_selected_flags(self) -> list[str]:
        """Get the names of the selected flags."""
        selected_flags = []
        for flag in self.flags:
            if self.flags[flag].checkState() == Qt.CheckState.Checked:
                selected_flags.append(flag)
        return selected_flags
    
    def get_flag_value(self, flag: str) -> bool:
        """Get the value of a flag."""
        return self.flags[flag].checkState() == Qt.CheckState.Checked

    def _on_flag_changed(self, item: QListWidgetItem) -> None:
        """Emit the onFlagChanged signal when a flag is changed."""
        # Get the flag name
        flag_name = item.text()
        # Get the flag value
        flag_value = item.checkState() == Qt.CheckState.Checked
        # Emit the signal
        self.onFlagChanged.emit(flag_name, flag_value)

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
        # Connect the itemChanged signal to the _on_flag_changed method
        self.lstFlagCheckboxes.itemChanged.connect(self._on_flag_changed)
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
        self.btn_select_all.clicked.connect(self.onSelectAllFlagsClicked.emit)
        # Add a 'Deselect All' button
        self.btn_deselect_all = QPushButton("Deselect All")
        buttons_layout.addWidget(self.btn_deselect_all)
        self.btn_deselect_all.clicked.connect(self.onDeselectAllFlagsClicked.emit)
        # Add an 'Invert Selection' button
        self.btn_invert_selection = QPushButton("Invert Selection")
        buttons_layout.addWidget(self.btn_invert_selection)
        self.btn_invert_selection.clicked.connect(self.onInvertSelectionFlagsClicked.emit)
        # Add a 'Clear Selection' button
        self.btn_clear_selection = QPushButton("Clear Selection")
        buttons_layout.addWidget(self.btn_clear_selection)
        self.btn_clear_selection.clicked.connect(self.onClearSelectionFlagsClicked.emit)
        # Push the buttons to the top
        buttons_layout.addStretch()
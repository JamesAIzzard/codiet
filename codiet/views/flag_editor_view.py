from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QPushButton
)
from PyQt6.QtCore import Qt


class FlagEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Build the UI
        self._build_ui()

        # Create a dict of the flag ui elements
        self.flags = {}

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

    def select_flag(self, flag: str):
        '''Update the flag to be selected.'''
        self.flags[flag].setCheckState(Qt.CheckState.Checked)

    def deselect_flag(self, flag: str):
        '''Update the flag to be deselected.'''
        self.flags[flag].setCheckState(Qt.CheckState.Unchecked)

    def deselect_all_flags(self):
        '''Deselect all flags.'''
        for flag in self.flags:
            self.flags[flag].setCheckState(Qt.CheckState.Unchecked)

    def invert_flag_selection(self, flag: str):
        '''Invert the selection of the flag.'''
        if self.flags[flag].checkState() == Qt.CheckState.Checked:
            self.flags[flag].setCheckState(Qt.CheckState.Unchecked)
        else:
            self.flags[flag].setCheckState(Qt.CheckState.Checked)
    
    def get_selected_flags(self) -> list[str]:
        '''Get a list of all the selected flags.'''
        selected_flags = []
        for flag in self.flags:
            if self.flags[flag].checkState() == Qt.CheckState.Checked:
                selected_flags.append(flag)
        return selected_flags
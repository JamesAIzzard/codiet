from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QListWidgetItem,
    QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal

from codiet.views import block_signals
from codiet.views.icon_button import IconButton


class FlagEditorView(QWidget):
    """The UI element to allow the user to edit flags."""

    # Define signals
    addFlagClicked = pyqtSignal()
    removeFlagClicked = pyqtSignal(int)
    flagChanged = pyqtSignal(int, bool)
    selectAllFlagsClicked = pyqtSignal()
    deselectAllFlagsClicked = pyqtSignal()
    invertFlagsClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Build the UI
        self._build_ui()

    @property
    def flags(self) -> dict[int, bool]:
        """Return a dictionary of currently represented flags
        and their corresponding states.

        Returns:
            dict[int, str]: A dictionary of flag IDs and their names.
        """
        # Grab the items and data from the list
        widgets_and_ids = self.flag_list.all_items_and_data
        # Each widget is a checkbox, convert this list to a dictionary
        # where the key is the flag ID and the value is the checkbox state
        flags = {}
        for widget, flag_id in widgets_and_ids:
            flags[flag_id] = widget.checkState() == Qt.CheckState.Checked
        return flags

    def read_flag(self, flag_id: int) -> bool:
        """Read the value of a flag."""
        # Grab the item by its id
        item = self.flag_list.get_item_for_data(flag_id)
        # Return the value of the checkbox
        return item.checkState() == Qt.CheckState.Checked

    def add_flag(self, flag_id: int, display_name: str) -> None:
        """Adds a flag to the list of checkable flags"""
        # If the flag is already in the list, raise an exception
        if self.flag_list.data_in_list(flag_id):
            raise ValueError(f"Flag {flag_id} is already in the list")
        # Create the item
        item = QListWidgetItem(display_name)
        # Make the item checkable
        item.setFlags(
            item.flags() | Qt.ItemFlag.ItemIsUserCheckable
        )
        # Set the item as initially unchecked
        item.setCheckState(Qt.CheckState.Unchecked)
        # Add the item to the UI
        self.flag_list.add_item(item, flag_id)

    def set_flag(self, flag_id: int, value: bool) -> None:
        """Set the value of a flag."""
        # Grab the item for the id
        item = self.flag_list.get_item_for_data(flag_id)
        with block_signals(self.flag_list):
            # Set the check state of the item
            item.setCheckState(Qt.CheckState.Checked if value else Qt.CheckState.Unchecked)

    def set_all_flags_true(self):
        """Select all flags."""
        for flag_id in self.flags:
            self.set_flag(flag_id, True) 

    def set_all_flags_false(self):
        """Deselect all flags."""
        for flag_id in self.flags:
            self.set_flag(flag_id, False)
    
    def invert_flags(self):
        """Invert the selection of all flags."""
        for flag_id in self.flags:
            self.set_flag(flag_id, not self.read_flag(flag_id))

    def _on_flag_changed(self, item: QListWidgetItem) -> None:
        """Emit the onFlagChanged signal when a flag is changed."""
        # Get the flag id associated with the item
        flag_id = self.flag_list.get_data_for_item(item)
        # Get the new value of the flag
        value = item.checkState() == Qt.CheckState.Checked
        # Emit the flagChanged signal
        self.flagChanged.emit(flag_id, value)

    def _build_ui(self):
        """Build the UI for the flag editor"""
        # Create a vertical layout for the widget
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)
        # Reduce the vertical padding in this layout
        lyt_top_level.setContentsMargins(0, 0, 0, 0)        
        # Put a group box inside the vertical layout
        grp_outer_box = QGroupBox("Flags")
        lyt_top_level.addWidget(grp_outer_box)

        # Create two columns, the LHS for a checkable list
        # and the RHS for the helper tools on buttons
        columns_layout = QHBoxLayout()
        grp_outer_box.setLayout(columns_layout)

        # Add a listbox of checkable items to the LHS column
        # self.flag_list = ListBox(parent=self)
        # # Connect the itemChanged signal to the _on_flag_changed method
        # self.flag_list.itemChanged.connect(self._on_flag_changed)
        # # Reduce padding at the top of the group box
        # columns_layout.setContentsMargins(5, 5, 5, 5)
        # columns_layout.addWidget(self.flag_list, 1)

        # Create a vertical list of buttons in the RHS column
        buttons_layout = QVBoxLayout()
        columns_layout.addLayout(buttons_layout, 0)
        # Add a horizontal row for the add and remove buttons
        add_remove_layout = QHBoxLayout()
        buttons_layout.addLayout(add_remove_layout)
        # Add an 'Add' button
        self.btn_add_flag = IconButton(icon_filename="add-icon.png")
        add_remove_layout.addWidget(self.btn_add_flag)
        self.btn_add_flag.clicked.connect(self.addFlagClicked.emit)
        # Add a 'Remove' button
        self.btn_remove_flag = IconButton(icon_filename="remove-icon.png")
        add_remove_layout.addWidget(self.btn_remove_flag)
        self.btn_remove_flag.clicked.connect(self.removeFlagClicked.emit)
        # Populate buttons column with helper buttons
        # Add a 'Select All' button
        self.btn_select_all = QPushButton("Select All")
        buttons_layout.addWidget(self.btn_select_all)
        self.btn_select_all.clicked.connect(self.selectAllFlagsClicked.emit)
        # Add a 'Deselect All' button
        self.btn_deselect_all = QPushButton("Deselect All")
        buttons_layout.addWidget(self.btn_deselect_all)
        self.btn_deselect_all.clicked.connect(self.deselectAllFlagsClicked.emit)
        # Add an 'Invert Selection' button
        self.btn_invert_selection = QPushButton("Invert Selection")
        buttons_layout.addWidget(self.btn_invert_selection)
        self.btn_invert_selection.clicked.connect(self.invertFlagsClicked.emit)
        # Push the buttons to the top
        buttons_layout.addStretch()
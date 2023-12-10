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


class IngredientFlagEditorView(QWidget):
    def __init__(self):
        super().__init__()

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
        self.listWidget = QListWidget()
        columns_layout.addWidget(self.listWidget, 1)

        # Create a vertical list of buttons in the RHS column
        buttons_layout = QVBoxLayout()
        columns_layout.addLayout(buttons_layout, 0)

        # Populate buttons column with helper buttons
        # Add a 'Select All' button
        self.select_all_button = QPushButton("Select All")
        buttons_layout.addWidget(self.select_all_button)
        # Add a 'Deselect All' button
        self.deselect_all_button = QPushButton("Deselect All")
        buttons_layout.addWidget(self.deselect_all_button)
        # Add an 'Invert Selection' button
        self.invert_selection_button = QPushButton("Invert Selection")
        buttons_layout.addWidget(self.invert_selection_button)
        # Add a 'Clear Selection' button
        self.clear_selection_button = QPushButton("Clear Selection")
        buttons_layout.addWidget(self.clear_selection_button)

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
        # Add the item
        self.listWidget.addItem(item)
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtGui import QFont

class RecipeTypesEditorView(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

        # Put some dummy recipe types in the editor for testing purposes
        dummy_recipe_types = ["Breakfast", "Lunch", "Dinner", "Snack"]
        self.update_recipe_types(dummy_recipe_types)

    def update_recipe_types(self, recipe_types: list[str]) -> None:
        """Update the recipe types in the editor."""
        # Clear the current recipe types
        self.listbox_recipe_types.clear()
        # Loop through the recipe types
        for recipe_type in recipe_types:
            # Add a new row to the list
            self.listbox_recipe_types.addItem(QListWidgetItem(recipe_type))

    def _build_ui(self):
        """Build the UI for the recipe types editor."""
        # Create a vertical layout for the page
        page_layout = QVBoxLayout()
        self.setLayout(page_layout)

        # Create a label and add it to the layout
        label = QLabel("Recipe Types Editor")
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        page_layout.addWidget(label)

        # Create a horizontal layout with two columns
        columns_layout = QHBoxLayout()
        page_layout.addLayout(columns_layout)

        # Add a first column with a vertical layout inside
        column1_layout = QVBoxLayout()
        columns_layout.addLayout(column1_layout, 2)

        # Add a second column with a vertical layout inside
        column2_layout = QVBoxLayout()
        columns_layout.addLayout(column2_layout, 3)

        # Underneath, add a listbox with recipe types inside
        self.listbox_recipe_types = QListWidget()
        column1_layout.addWidget(self.listbox_recipe_types)

        # In the second column, add an 'Add Recipe Type' button
        button_add_recipe_type = QPushButton("Add Recipe Type")
        column2_layout.addWidget(button_add_recipe_type)
        # In the second column, add a 'Remove Recipe Type' button
        button_remove_recipe_type = QPushButton("Remove Recipe Type")
        column2_layout.addWidget(button_remove_recipe_type)
        # Also add a 'Rename Recipe Type' button
        button_rename_recipe_type = QPushButton("Rename Recipe Type")
        column2_layout.addWidget(button_rename_recipe_type)
        # Push the buttons to the top of the column
        column2_layout.addStretch()


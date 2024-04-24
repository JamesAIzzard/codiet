from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QListWidget,
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QPushButton
)

class RecipeTypeEditorView(QWidget):
    """UI element to allow the user to select/deselect recipe types."""
    def __init__(self):
        super().__init__()
        self._build_ui()

    def update_recipe_types(self, recipe_types: list[str]) -> None:
        """Update the recipe types available in the editor."""
        # Clear the current recipe types
        self.lst_recipe_types.clear()
        # Add the new recipe types
        for recipe_type in recipe_types:
            item = QListWidgetItem(recipe_type)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.lst_recipe_types.addItem(item)

    def update_recipe_types_selection(self, selected_recipe_types: dict[str, bool]) -> None:
        """Update the recipe types which are selected in the editor."""
        # Iterate through the selected recipe types
        for recipe_type, selected in selected_recipe_types.items():
            # Update the selection of the recipe type
            self.update_recipe_type_selection(recipe_type, selected)

    def update_recipe_type_selection(self, recipe_type: str, selected: bool) -> None:
        """Update the selection of a single recipe type."""
        # Fetch the recipe type matching the name
        item = self._fetch_recipe_type_item(recipe_type)
        # Set the checked status
        item.setCheckState(Qt.CheckState.Checked if selected else Qt.CheckState.Unchecked)

    def _build_ui(self):
        """Build the UI for the recipe type editor."""
        # Create a vertical layout for the page
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)
        # Remove all margins
        lyt_top_level.setContentsMargins(0, 0, 0, 0)

        # Add a groupbox for the recipe types
        gb_recipe_types = QGroupBox("Recipe Types")
        lyt_top_level.addWidget(gb_recipe_types)
        lyt_recipe_types = QVBoxLayout()
        gb_recipe_types.setLayout(lyt_recipe_types)
        lyt_recipe_types.setContentsMargins(5, 5, 5, 5)

        # Add a horizontal layout for buttons to add/remove recipe types
        lyt_buttons = QHBoxLayout()
        lyt_recipe_types.addLayout(lyt_buttons)
        # Add an 'Add' button
        btn_add = QPushButton("Add")
        lyt_buttons.addWidget(btn_add)
        # Add a 'Remove' button
        btn_remove = QPushButton("Remove")
        lyt_buttons.addWidget(btn_remove)

        # Add a listbox for the recipe types
        self.lst_recipe_types = QListWidget()
        lyt_recipe_types.addWidget(self.lst_recipe_types)

    def _fetch_recipe_type_item(self, recipe_type: str) -> QListWidgetItem:
        """Fetch the QListWidgetItem for a recipe type."""
        # Iterate through the recipe types
        for i in range(self.lst_recipe_types.count()):
            item = self.lst_recipe_types.item(i)
            # Assert item is not None to satisfy type checker
            assert item is not None
            # Check if the item text matches the recipe type
            if item.text() == recipe_type:
                # If it does, return the item
                return item
        # If the recipe type is not found, raise an error
        raise ValueError(f"Recipe type '{recipe_type}' not found in the list.")


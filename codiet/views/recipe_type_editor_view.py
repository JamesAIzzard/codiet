from PyQt6.QtCore import pyqtSignal
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
    # Define signals
    addRecipeTypeClicked = pyqtSignal()
    removeRecipeTypeClicked = pyqtSignal()


    """UI element to allow the user to select/deselect recipe types."""
    def __init__(self):
        super().__init__()
        self._build_ui()

        # Emit the button press signals
        self.btn_add.clicked.connect(self.addRecipeTypeClicked.emit)
        self.btn_remove.clicked.connect(self.removeRecipeTypeClicked.emit)

    @property
    def selected_recipe_type(self) -> str | None:
        """Return the selected recipe type."""
        current_item = self.lst_recipe_types.currentItem()
        if current_item is not None:
            return current_item.text()
        return None
    
    def recipe_type_in_list(self, recipe_type: str) -> bool:
        """Check if a recipe type is in the list."""
        try:
            self._fetch_recipe_type_item(recipe_type)
            return True
        except ValueError:
            return False

    def add_recipe_type(self, recipe_type: str) -> None:
        """Add a recipe type to the list."""
        self.lst_recipe_types.addItem(recipe_type)

    def remove_recipe_type(self, recipe_type: str) -> None:
        """Remove a recipe type from the list."""
        item = self._fetch_recipe_type_item(recipe_type)
        self.lst_recipe_types.takeItem(self.lst_recipe_types.row(item))

    def update_recipe_types(self, recipe_types: list[str]) -> None:
        """Update the recipe types available in the editor."""
        # Clear the current recipe types
        self.lst_recipe_types.clear()
        # Add the new recipe types
        for recipe_type in recipe_types:
            if not self.recipe_type_in_list(recipe_type):
                self.add_recipe_type(recipe_type)

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
        self.btn_add = QPushButton("Add")
        lyt_buttons.addWidget(self.btn_add)
        # Add a 'Remove' button
        self.btn_remove = QPushButton("Remove")
        lyt_buttons.addWidget(self.btn_remove)

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


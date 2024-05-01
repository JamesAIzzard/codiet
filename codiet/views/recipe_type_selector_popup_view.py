from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget
from PyQt6.QtCore import pyqtSignal

from codiet.views.search_views import SearchTermView

class RecipeTypeSelectorPopupView(QDialog):
    # Define signals
    recipeTypeSelected = pyqtSignal(str)
    searchTermChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._build_ui()

        # Emit the recipeTypeSelected signal when a search item is clicked
        self.lst_recipe_types.itemClicked.connect(self._on_recipe_type_clicked)
        # Emit the searchTermChanged signal when the search box text changes
        self.search_box.searchTermChanged.connect(self.searchTermChanged.emit)

    @property
    def selected_recipe_type(self) -> str | None:
        """Return the selected recipe type."""
        # Get the selected item
        selected_item = self.lst_recipe_types.currentItem()
        # If there is no selected item, return an empty string
        if selected_item is None:
            return None
        # Return the text of the selected item
        return selected_item.text()

    def recipe_type_in_list(self, recipe_type: str) -> bool:
        """Check if a recipe type is in the list."""
        for i in range(self.lst_recipe_types.count()):
            item = self.lst_recipe_types.item(i)
            if item is not None and item.text() == recipe_type:
                return True
        return False

    def add_recipe_type(self, recipe_type: str) -> None:
        """Add a recipe type to the list."""
        if not self.recipe_type_in_list(recipe_type):
            self.lst_recipe_types.addItem(recipe_type)

    def update_recipe_types(self, recipe_types: list[str]) -> None:
        """Update the recipe types in the list."""
        # Clear the current recipe types
        self.lst_recipe_types.clear()
        # Add the new recipe types
        for recipe_type in recipe_types:
            self.add_recipe_type(recipe_type)

    def clear_recipe_types(self) -> None:
        """Clear the recipe types from the list."""
        self.lst_recipe_types.clear()

    def _on_recipe_type_clicked(self, item) -> None:
        """Handler for click on recipe type."""
        self.recipeTypeSelected.emit(self.selected_recipe_type)

    def _build_ui(self):
        """Build the user interface."""
        self.setWindowTitle("Recipe Type Selector")
        self.resize(400, 300)

        # Create a layout for the dialog
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a search box and add it to the layout
        self.search_box = SearchTermView()
        layout.addWidget(self.search_box)

        # Create a listbox and add it to the layout
        self.lst_recipe_types = QListWidget()
        layout.addWidget(self.lst_recipe_types)

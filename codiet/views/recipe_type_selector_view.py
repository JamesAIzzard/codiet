from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QListWidget,
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
)

class RecipeTypeSelectorView(QWidget):
    """UI element to allow the user to select/deselect recipe types."""
    def __init__(self):
        super().__init__()

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

        # Add a listbox for the recipe types
        self.lst_recipe_types = QListWidget()
        lyt_recipe_types.addWidget(self.lst_recipe_types)

        # Add a list of recipe types with checkboxes
        recipe_types = ["Main", "Side", "Drink", "Snack"]
        for recipe_type in recipe_types:
            item = QListWidgetItem(recipe_type)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.lst_recipe_types.addItem(item)


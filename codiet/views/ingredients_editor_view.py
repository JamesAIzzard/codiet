from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)

from codiet.views.ingredient_quantity_editor_view import IngredientQuantityEditorView
from codiet.views.ingredient_search_popup_view import IngredientSearchPopupView

class IngredientsEditorView(QWidget):
    def __init__(self):
        super().__init__()
        # Build the UI
        self._build_ui()
        # Init the ingredients search popup
        self.ingredient_search_popup = IngredientSearchPopupView()

    def update_ingredients(self, ingredients: dict[str, dict]) -> None:
        """Update the ingredients in the editor."""
        # Clear the current ingredients
        self.list_ingredients.clear()
        # Loop through the ingredients
        for ingredient_name, ingredient_data in ingredients.items():
            # Add a new row to the list
            listItem = QListWidgetItem(self.list_ingredients)
            # Create a new instance of IngredientQuantityEditorView
            ingredient = IngredientQuantityEditorView(ingredient_name)
            # Set the size hint of the list item to the size hint of the ingredient editor
            listItem.setSizeHint(ingredient.sizeHint())
            # Add the list item to the list
            self.list_ingredients.addItem(listItem)
            # Set the widget of the list item to be the ingredient editor
            self.list_ingredients.setItemWidget(listItem, ingredient)

    def show_ingredient_search_popup(self) -> None:
        """Show the ingredient search popup."""
        self.ingredient_search_popup.show()

    def _build_ui(self):
        """Build the UI for the ingredients editor."""
        # Create vertical layout as the top level
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)
        # Reduce the vertical padding in this layout
        lyt_top_level.setContentsMargins(0, 0, 0, 0)

        # Create a groupbox inside this layout
        grp_ingredients = QGroupBox("Ingredients")
        lyt_top_level.addWidget(grp_ingredients)
        lyt_main = QVBoxLayout()
        grp_ingredients.setLayout(lyt_main)
        lyt_main.setContentsMargins(5, 5, 5, 5)

        # Add a horizontal button to the main layout to hold the buttons
        lyt_buttons = QHBoxLayout()
        lyt_main.addLayout(lyt_buttons)

        # Create an add ingredient button
        self.btn_add_ingredient = QPushButton("Add")
        lyt_buttons.addWidget(self.btn_add_ingredient)
        # Create a remove ingredient button
        self.btn_remove_ingredient = QPushButton("Remove")
        lyt_buttons.addWidget(self.btn_remove_ingredient)

        # Create a list widget to hold the ingredients
        self.list_ingredients = QListWidget()
        lyt_main.addWidget(self.list_ingredients)
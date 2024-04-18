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

class IngredientsEditorView(QWidget):
    def __init__(self):
        super().__init__()
        # Build the UI
        self._build_ui()

    @property
    def selected_ingredient_widget(self) -> IngredientQuantityEditorView | None:
        """Return the selected ingredient widget."""
        # Get the selected list item
        selected_item = self.list_ingredients.currentItem()
        # If there is no selected item, return None
        if selected_item is None:
            return None
        # Grab the widget from the item
        selected_widget = self.list_ingredients.itemWidget(selected_item)
        # Return the widget
        return selected_widget # type: ignore

    @property
    def selected_ingredient_id(self) -> int | None:
        """Return the selected ingredient."""
        # First grab the widget
        widget = self.selected_ingredient_widget
        # If there is no widget, return None
        if widget is None:
            return None
        # Return the ingredient ID
        return widget.ingredient_id

    def update_ingredients(self, ingredients: dict[str, dict]) -> None:
        """Update the ingredients in the editor."""
        # Clear the current ingredients
        self.list_ingredients.clear()
        # Loop through the ingredients
        for ingredient_name, ingredient_data in ingredients.items():
            # Add the ingredient to the list
            self.add_ingredient(
                ingredient_name=ingredient_name,
                ingredient_id=ingredient_data["id"],
                ingredient_qty=ingredient_data["qty"],
                ingredient_qty_unit=ingredient_data["qty_unit"],
                ingredient_qty_utol=ingredient_data["qty_utol"],
                ingredient_qty_ltol=ingredient_data["qty_ltol"]
            )

    def add_ingredient(self, 
            ingredient_name: str,
            ingredient_id: int,
            ingredient_qty: float | None = None,
            ingredient_qty_unit: str = "g",
            ingredient_qty_utol: float | None = None,
            ingredient_qty_ltol: float | None = None
        ) -> None:
        """Add an ingredient to the list."""
        # Create a new row in the list
        listItem = QListWidgetItem(self.list_ingredients)
        # Create a new instance of IngredientQuantityEditorView
        ingredient = IngredientQuantityEditorView(
            ingredient_name, 
            ingredient_id,
            ingredient_qty,
            ingredient_qty_unit,
            ingredient_qty_utol,
            ingredient_qty_ltol
        )
        # Set the size hint of the list item to the size hint of the ingredient editor
        listItem.setSizeHint(ingredient.sizeHint())
        # Add the list item to the list
        self.list_ingredients.addItem(listItem)
        # Set the widget of the list item to be the ingredient editor
        self.list_ingredients.setItemWidget(listItem, ingredient)

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
from PyQt6.QtCore import pyqtSignal, QVariant
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
    """UI element to allow the user to edit ingredients associated with a recipe."""

    # Define signals
    addIngredientClicked = pyqtSignal()
    removeIngredientClicked = pyqtSignal()
    ingredientQtyChanged = pyqtSignal(int, QVariant)
    ingredientQtyUnitChanged = pyqtSignal(int, QVariant)
    ingredientQtyUTolChanged = pyqtSignal(int, QVariant)
    ingredientQtyLTolChanged = pyqtSignal(int, QVariant)

    def __init__(self):
        super().__init__()
        # Build the UI
        self._build_ui()

        # Create a list to hold the ingredient quantities
        # indexed by the ingredient ID.
        self._ingredient_quantities: dict[int, IngredientQuantityEditorView] = {}

        # Emit the button press signals
        self.btn_add_ingredient.clicked.connect(self.addIngredientClicked.emit)
        self.btn_remove_ingredient.clicked.connect(self.removeIngredientClicked.emit)

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
        return selected_widget  # type: ignore

    @property
    def selected_ingredient_id(self) -> int | None:
        """Return the selected ingredient id."""
        # First grab the widget
        widget = self.selected_ingredient_widget
        # If there is no widget, return None
        if widget is None:
            return None
        # Return the ingredient ID
        return widget.ingredient_id

    def add_ingredient_quantity(
        self,
        ingredient_name: str,
        ingredient_id: int,
        ingredient_quantity_value: float | None = None,
        ingredient_quantity_unit: str = "g",
        ingredient_quantity_upper_tol: float | None = None,
        ingredient_quantity_lower_tol: float | None = None,
    ) -> None:
        """Add an ingredient quantity to the list."""
        # Create a new row in the list
        listItem = QListWidgetItem(self.list_ingredients)
        # Create a new instance of IngredientQuantityEditorView
        ingredient_qty_editor = IngredientQuantityEditorView(
            ingredient_name=ingredient_name,
            ingredient_id=ingredient_id,
        )
        # Set the values
        ingredient_qty_editor.ingredient_qty_value = ingredient_quantity_value
        ingredient_qty_editor.ingredient_qty_unit = ingredient_quantity_unit
        ingredient_qty_editor.ingredient_qty_utol = ingredient_quantity_upper_tol
        ingredient_qty_editor.ingredient_qty_ltol = ingredient_quantity_lower_tol
        # Add it to the internal dict
        self._ingredient_quantities[ingredient_id] = ingredient_qty_editor
        # Set the size hint of the list item to the size hint of the ingredient editor
        listItem.setSizeHint(ingredient_qty_editor.sizeHint())
        # Add the list item to the list
        self.list_ingredients.addItem(listItem)
        # Set the widget of the list item to be the ingredient editor
        self.list_ingredients.setItemWidget(listItem, ingredient_qty_editor)
        # Connect the signals
        ingredient_qty_editor.ingredientQtyChanged.connect(
            lambda value: self.ingredientQtyChanged.emit(ingredient_id, value)
        )
        ingredient_qty_editor.ingredientQtyUnitChanged.connect(
            lambda value: self.ingredientQtyUnitChanged.emit(ingredient_id, value)
        )
        ingredient_qty_editor.ingredientQtyUTolChanged.connect(
            lambda value: self.ingredientQtyUTolChanged.emit(ingredient_id, value)
        )
        ingredient_qty_editor.ingredientQtyLTolChanged.connect(
            lambda value: self.ingredientQtyLTolChanged.emit(ingredient_id, value)
        )

    def remove_ingredient_quantity(self, ingredient_id: int) -> None:
        """Remove an ingredient from the list."""
        # Get the ingredient editor
        ingredient_quantity_editor = self._ingredient_quantities[ingredient_id]
        # Iterate through each item on the list
        for i in range(self.list_ingredients.count()):
            # Get the list item
            list_item = self.list_ingredients.item(i)
            # Get the widget from the list item
            widget = self.list_ingredients.itemWidget(list_item)
            # If the widget is the same as the ingredient editor, remove the list item
            if widget == ingredient_quantity_editor:
                self.list_ingredients.takeItem(i)
                break
        # Remove the ingredient from the internal dict
        del self._ingredient_quantities[ingredient_id]

    def update_ingredient_quantity_value(
        self, ingredient_id: int, quantity_value: float | None
    ) -> None:
        """Update the quantity value of an ingredient."""
        # Get the ingredient editor
        ingredient_editor = self._ingredient_quantities[ingredient_id]
        # Update the quantity value
        ingredient_editor.ingredient_qty_value = quantity_value

    def update_ingredient_quantity_unit(
        self, ingredient_id: int, quantity_unit: str
    ) -> None:
        """Update the quantity unit of an ingredient."""
        # Get the ingredient editor
        ingredient_editor = self._ingredient_quantities[ingredient_id]
        # Update the quantity unit
        ingredient_editor.ingredient_qty_unit = quantity_unit

    def update_ingredient_quantity_upper_tol(
        self, ingredient_id: int, upper_tol: float | None
    ) -> None:
        """Update the upper tolerance of an ingredient."""
        # Get the ingredient editor
        ingredient_editor = self._ingredient_quantities[ingredient_id]
        # Update the upper tolerance
        ingredient_editor.ingredient_qty_utol = upper_tol

    def update_ingredient_quantity_lower_tol(
        self, ingredient_id: int, lower_tol: float | None
    ) -> None:
        """Update the lower tolerance of an ingredient."""
        # Get the ingredient editor
        ingredient_editor = self._ingredient_quantities[ingredient_id]
        # Update the lower tolerance
        ingredient_editor.ingredient_qty_ltol = lower_tol

    def remove_all_ingredients(self) -> None:
        """Clear all the ingredients from the list."""
        self.list_ingredients.clear()

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

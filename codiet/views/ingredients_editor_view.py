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

        # Add some dummy instances of IngredientQuantiyEditorView for now
        # Create a list of dummy ingredient names
        dummy_ingredient_names = ["Ingredient 1", "Ingredient 2", "Ingredient 3"]
        # Loop through the dummy ingredient names
        for ingredient_name in dummy_ingredient_names:
            # Add a new row to the list
            listItem = QListWidgetItem(self.list_ingredients)
            # Create a new instance of IngredientQuantityEditorView
            dummy_ingredient = IngredientQuantityEditorView(ingredient_name)
            # Set the size hint of the list item to the size hint of the ingredient editor
            listItem.setSizeHint(dummy_ingredient.sizeHint())
            # Add the list item to the list
            self.list_ingredients.addItem(listItem)
            # Set the widget of the list item to be the ingredient editor
            self.list_ingredients.setItemWidget(listItem, dummy_ingredient)
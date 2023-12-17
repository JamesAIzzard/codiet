from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
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
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Reduce the vertical padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a groupbox inside this layout
        ingredients_group = QGroupBox("Ingredients")
        layout.addWidget(ingredients_group)
        ingredients_layout = QVBoxLayout()
        ingredients_group.setLayout(ingredients_layout)
        ingredients_layout.setContentsMargins(5, 5, 5, 5)

        # Create an add ingredient button
        self.btn_add_ingredient = QPushButton("Add Ingredient")
        ingredients_layout.addWidget(self.btn_add_ingredient)

        # Create a list widget to hold the ingredients
        self.list_ingredients = QListWidget()
        ingredients_layout.addWidget(self.list_ingredients)

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
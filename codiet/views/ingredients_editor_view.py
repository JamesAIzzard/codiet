from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QPushButton,
    QListWidget,
)

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
        # Add some dummy ingredients for now
        self.list_ingredients.addItem("Ingredient 1")
        self.list_ingredients.addItem("Ingredient 2")
        self.list_ingredients.addItem("Ingredient 3")
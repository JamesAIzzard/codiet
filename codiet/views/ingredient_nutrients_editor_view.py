from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)

from codiet.views.ingredient_nutrient_editor_view import IngredientNutrientEditorView

class IngredientNutrientsEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create vertical layout as the top level
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Reduce the vertical padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Put a group inside this layout
        group_box = QGroupBox("Nutrients")
        layout.addWidget(group_box)

        # Put a vertical layout inside the group box
        rows_layout = QVBoxLayout()
        group_box.setLayout(rows_layout)

        # Create an 'Add Nutrient' button
        self.add_nutrient_button = QPushButton("Add Nutrient")
        rows_layout.addWidget(self.add_nutrient_button)

        # Create a listbox for the nutrient rows
        self.listWidget = QListWidget()
        rows_layout.addWidget(self.listWidget)

    def add_nutrient(self, nutrient_name: str):
        # Add a new row to the list
        listItem = QListWidgetItem(self.listWidget)
        nutrient_widget = IngredientNutrientEditorView(nutrient_name)
        listItem.setSizeHint(nutrient_widget.sizeHint())
        self.listWidget.addItem(listItem)
        self.listWidget.setItemWidget(listItem, nutrient_widget)
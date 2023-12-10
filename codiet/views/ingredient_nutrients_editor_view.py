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

        # Add custom widgets to the list
        for nutr_name in ["Protein", "Carbohydrate", "Trans Fat"]:  # Example with 5 custom widgets
            listItem = QListWidgetItem(self.listWidget)
            nutrient_widget = IngredientNutrientEditorView(nutr_name)
            listItem.setSizeHint(nutrient_widget.sizeHint())  # Important to set the size hint
            self.listWidget.addItem(listItem)
            self.listWidget.setItemWidget(listItem, nutrient_widget)
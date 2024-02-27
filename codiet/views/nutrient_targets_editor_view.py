from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)

from codiet.views.nutrient_target_editor_view import NutrientTargetEditorView

class NutrientTargetsEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create vertical layout as the top level
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)
        # Reduce the vertical padding in this layout
        lyt_top_level.setContentsMargins(0, 0, 0, 0)

        # Put a group inside this layout
        group_box = QGroupBox("Nutrient Targets")
        lyt_top_level.addWidget(group_box)

        # Put a vertical layout inside the group box
        lyt_rows = QVBoxLayout()
        group_box.setLayout(lyt_rows)
        lyt_rows.setContentsMargins(5, 5, 5, 5)

        # In the first row, add a HBox for buttons
        lyt_buttons = QHBoxLayout()
        lyt_rows.addLayout(lyt_buttons)
        self.add_nutrient_button = QPushButton("Add")
        lyt_buttons.addWidget(self.add_nutrient_button)
        self.remove_nutrient_button = QPushButton("Remove")
        lyt_buttons.addWidget(self.remove_nutrient_button)

        # Create a listbox for the nutrient rows
        self.listWidget = QListWidget()
        lyt_rows.addWidget(self.listWidget)

        # Add some dummy nutrients
        self.add_target_nutrient("Protein")
        self.add_target_nutrient("Fat")
        self.add_target_nutrient("Carbohydrate")

    def add_target_nutrient(self, nutrient_name: str):
        # Add a new row to the list
        listItem = QListWidgetItem(self.listWidget)
        nutrient_widget = NutrientTargetEditorView(nutrient_name)
        listItem.setSizeHint(nutrient_widget.sizeHint())
        self.listWidget.addItem(listItem)
        self.listWidget.setItemWidget(listItem, nutrient_widget)
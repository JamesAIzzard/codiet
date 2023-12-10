from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)

from codiet.views.ingredient_name_editor_view import IngredientNameEditorView
from codiet.views.ingredient_cost_editor_view import IngredientCostEditorView

class IngredientBasicInfoEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create vertical layout as the top level
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Reduce the vertical padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Put a group inside this layout
        group_box = QGroupBox("Basic Info")
        layout.addWidget(group_box)

        # Put a vertical layout inside the group box
        rows_layout = QVBoxLayout()
        group_box.setLayout(rows_layout)

        # Bring in the name and cost editors
        self.name_editor = IngredientNameEditorView()
        rows_layout.addWidget(self.name_editor)
        self.cost_editor = IngredientCostEditorView()
        rows_layout.addWidget(self.cost_editor)


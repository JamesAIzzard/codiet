from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QPushButton,
)

from codiet.views.ingredient_density_editor_view import IngredientDensityEditorView
from codiet.views.ingredient_pc_mass_editor_view import IngredientPcMassEditorView

class IngredientBulkPropertiesEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout as the top level
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        # Put a group inside this layout
        group_box = QGroupBox("Bulk Properties")
        layout.addWidget(group_box)

        # Put a vertical layout inside the group box
        rows_layout = QVBoxLayout()
        group_box.setLayout(rows_layout)

        # Bring in the density and pc mass editors
        self.density_editor = IngredientDensityEditorView()
        rows_layout.addWidget(self.density_editor)
        self.pc_mass_editor = IngredientPcMassEditorView()
        rows_layout.addWidget(self.pc_mass_editor)
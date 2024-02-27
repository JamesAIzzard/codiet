from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QSizePolicy
)
from PyQt6.QtCore import Qt

class IngredientQuantityEditorView(QWidget):
    def __init__(self, ingredient_name: str):
        super().__init__()

        # Create a horizontal layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create a label and add it to the layout
        label = QLabel(ingredient_name)
        layout.addWidget(label)

        # Add a stretch
        layout.addStretch(1)

        # Create a textbox for the ingredient quantity
        self.txtIngredientQuantity = QLineEdit()
        # Set the max width of the textbox
        self.txtIngredientQuantity.setMaximumWidth(60)
        layout.addWidget(self.txtIngredientQuantity)

        # Create a dropdown for qty units
        self.cmbIngredientQuantityUnits = QComboBox()
        # Add some units to the dropdown
        # These will utimately get pulled from a config
        # TODO - pull units from config
        self.cmbIngredientQuantityUnits.addItems(["g", "kg", "lb"])
        layout.addWidget(self.cmbIngredientQuantityUnits)

        # Create a vertical layout for tolerances
        tolerance_layout = QVBoxLayout()
        # Remove the padding
        tolerance_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(tolerance_layout)
        # Create a horizontal layout for the upper tol
        upper_tol_layout = QHBoxLayout()
        tolerance_layout.addLayout(upper_tol_layout)
        # Add a plus label
        label = QLabel("+")
        # Set the width
        label.setMaximumWidth(10)
        # Centre the text in the label
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upper_tol_layout.addWidget(label)
        # Add a textbox
        self.txtUpperTolerance = QLineEdit()
        # Set the max width of the textbox
        self.txtUpperTolerance.setMaximumWidth(30)
        upper_tol_layout.addWidget(self.txtUpperTolerance)
        # Add a label for '%'
        label = QLabel("%")
        upper_tol_layout.addWidget(label)
        # Create a horizontal layout for the lower tol
        lower_tol_layout = QHBoxLayout()
        tolerance_layout.addLayout(lower_tol_layout)
        # Add a - label
        label = QLabel("-")
        # Set the width
        label.setMaximumWidth(10)
        # Centre the text in the label
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lower_tol_layout.addWidget(label)
        # Add a textbox
        self.txtLowerTolerance = QLineEdit()
        # Set the max width of the textbox
        self.txtLowerTolerance.setMaximumWidth(30)
        lower_tol_layout.addWidget(self.txtLowerTolerance)
        # Add a label for '%'
        label = QLabel("%")
        lower_tol_layout.addWidget(label)

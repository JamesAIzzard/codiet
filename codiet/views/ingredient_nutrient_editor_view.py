from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton
)


class IngredientNutrientEditorView(QWidget):
    def __init__(self, nutrient_name: str):
        super().__init__()

        # Create a horizontal layout for the widget
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Reduce the horizontal padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a label and add it to the layout
        label = QLabel(nutrient_name + ":") 
        layout.addWidget(label)

        # Add a stretch
        layout.addStretch(1)

        # Create a textbox for nutrient mass
        self.txtNutrientMass = QLineEdit()
        # Limit the textbox to 10 chars
        self.txtNutrientMass.setMaximumWidth(60)
        layout.addWidget(self.txtNutrientMass)

        # Create a dropdown for mass units
        self.cmbMassUnits = QComboBox()
        # Add some mass units to the dropdown
        # These will utimately get pulled from a config
        # TODO - pull mass units from config
        self.cmbMassUnits.addItems(["g", "mg", "µg"])
        layout.addWidget(self.cmbMassUnits)

        # Create a label
        label = QLabel(" per ")
        layout.addWidget(label)

        # Create a textbox for ignredient mass
        self.txtIngredientMass = QLineEdit()
        # Set the max width of the textbox
        self.txtIngredientMass.setMaximumWidth(60)
        layout.addWidget(self.txtIngredientMass)
        
        # Create a dropdown for mass units
        self.cmbIngredientMassUnits = QComboBox()
        # Add some mass units to the dropdown
        # These will utimately get pulled from a config
        # TODO - pull mass units from config
        self.cmbIngredientMassUnits.addItems(["g", "kg"])
        layout.addWidget(self.cmbIngredientMassUnits)

        # Add a little space at either end of the widget
        layout.setContentsMargins(5, 0, 5, 0)

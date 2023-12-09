from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox

class IngredientDensityEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a horizontal layout for the widget
        layout = QHBoxLayout()

        # Create a label and add it to the layout
        label = QLabel("Density:")
        layout.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_density = QLineEdit()
        layout.addWidget(self.txt_density)

        # Create a volume units dropdown and add it to the layout
        self.cmb_vol_units = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_vol_units.addItems(["ml", "l"])
        layout.addWidget(self.cmb_vol_units)

        # Create another label and add it to the layout
        label = QLabel(" weighs ")
        layout.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_mass = QLineEdit()
        layout.addWidget(self.txt_mass)

        # Create a mass units dropdown and add it to the layout
        self.cmb_mass_units = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_mass_units.addItems(["g", "kg"])
        layout.addWidget(self.cmb_mass_units)

        # Reduce the vertical padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Set the layout for the widget
        self.setLayout(layout)
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, QGroupBox

class IngredientPcMassEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a horizontal layout for the widget
        layout = QHBoxLayout()

        # Create a label and add it to the layout
        label = QLabel("Piece Mass:")
        layout.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_piece_qty = QLineEdit()
        layout.addWidget(self.txt_piece_qty)

        # Create another label
        label = QLabel(" piece(s) weighs ")
        layout.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_piece_mass = QLineEdit()
        layout.addWidget(self.txt_piece_mass)

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
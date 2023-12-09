from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox

class IngredientCostEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a horizontal layout for the widget
        layout = QHBoxLayout()

        # Create the first label
        label = QLabel("Cost: £")
        layout.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_cost = QLineEdit()
        layout.addWidget(self.txt_cost)

        # Create a second label
        label = QLabel(" per ")
        layout.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_quantity = QLineEdit()
        layout.addWidget(self.txt_quantity)

        # Create a units dropdown
        self.cmb_units = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_units.addItems(["g", "kg", "ml", "l"])
        layout.addWidget(self.cmb_units)

        # Reduce the vertical padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Set the layout for the widget
        self.setLayout(layout)
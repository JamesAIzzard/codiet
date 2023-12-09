from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class IngredientEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the page
        layout = QVBoxLayout()

        # Create a label and add it to the layout
        label = QLabel("Ingredient Editor")
        layout.addWidget(label)

        # Add some spacing to the layout
        layout.addStretch(1)

        # Set the layout for the page
        self.setLayout(layout)
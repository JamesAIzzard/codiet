from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

class IngredientNameEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a horizontal layout for the widget
        layout = QHBoxLayout()

        # Create a label and add it to the layout
        label = QLabel("Name:")
        layout.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_name = QLineEdit()
        layout.addWidget(self.txt_name)

        # Reduce the vertical padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Set the layout for the widget
        self.setLayout(layout)
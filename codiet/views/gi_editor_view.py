from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox

class GIEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the widget
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Reduce the horizontal padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a top level groupbox
        group_box = QGroupBox("GI")
        layout.addWidget(group_box)

        # Put a horizontal layout inside the group box
        column_layout = QHBoxLayout()
        group_box.setLayout(column_layout)

        # Create a label and add it to the layout
        label = QLabel("Glycemic Index (Carbohydrate Only):")
        column_layout.addWidget(label)

        # Create a line edit and add it to the layout
        self.lineEdit = QLineEdit()
        column_layout.addWidget(self.lineEdit)
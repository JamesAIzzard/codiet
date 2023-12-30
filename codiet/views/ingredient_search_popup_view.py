from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QListWidget, QPushButton
from PyQt6.QtWidgets import QSizePolicy

class IngredientSearchPopupView(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Find Ingredient")
        self.resize(400, 300)

        # Create a layout for the dialog
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a search textbox and add it to the layout
        self.search_textbox = QLineEdit()
        layout.addWidget(self.search_textbox)

        # Create a dropdown and add it to the layout
        self.lst_search_results = QListWidget()
        # Make the dropdown fill the space
        self.lst_search_results.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.lst_search_results)

        # Add a button to the bottom saying open
        self.btn_open = QPushButton("Open")
        layout.addWidget(self.btn_open)

    def show(self):
        self.exec()

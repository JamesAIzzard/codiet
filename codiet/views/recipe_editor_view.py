from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QLineEdit
)
from PyQt6.QtGui import QFont

class RecipeEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the page
        page_layout = QVBoxLayout()
        self.setLayout(page_layout)

        # Create a label and add it to the layout
        label = QLabel("Recipe Editor")
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        page_layout.addWidget(label)

        # Create a horizontal layout for the columns
        columns_layout = QHBoxLayout()
        page_layout.addLayout(columns_layout)

        # Create the first column
        column1_layout = QVBoxLayout()
        columns_layout.addLayout(column1_layout, 2)

        # Add a row containg the recipe name label and a textbox
        recipe_name_layout = QHBoxLayout()
        column1_layout.addLayout(recipe_name_layout)
        label = QLabel("Recipe Name")
        recipe_name_layout.addWidget(label)
        self.textbox_recipe_name = QLineEdit()
        recipe_name_layout.addWidget(self.textbox_recipe_name)

        # Add a row containing the recipe instructions label and multiline textbox
        label = QLabel("Recipe Instructions")
        column1_layout.addWidget(label)
        self.textbox_recipe_instructions = QLineEdit()
        column1_layout.addWidget(self.textbox_recipe_instructions)

        # Create the second column
        column2_layout = QVBoxLayout()
        columns_layout.addLayout(column2_layout, 2)

        # Label the ingredients column
        label = QLabel("Ingredients")
        column2_layout.addWidget(label)

        # Create an add ingredient button
        self.btn_add_ingredient = QPushButton("Add Ingredient")
        column2_layout.addWidget(self.btn_add_ingredient)

        # Create a list widget to hold the ingredients
        self.list_ingredients = QListWidget()
        column2_layout.addWidget(self.list_ingredients)
        # Add some dummy ingredients for now
        self.list_ingredients.addItem("Ingredient 1")
        self.list_ingredients.addItem("Ingredient 2")
        self.list_ingredients.addItem("Ingredient 3")

        # Create the third column
        column3_layout = QVBoxLayout()
        columns_layout.addLayout(column3_layout, 1)

        # Create the Time Windows label
        label = QLabel("Time Windows")
        column3_layout.addWidget(label)

        # Create a button to add a time window
        self.btn_add_time_window = QPushButton("Add Time Window")
        column3_layout.addWidget(self.btn_add_time_window)

        # Create a list widget to hold the time windows
        self.list_time_windows = QListWidget()
        column3_layout.addWidget(self.list_time_windows)
        # Add some dummy time windows for now
        self.list_time_windows.addItem("Time Window 1")
        self.list_time_windows.addItem("Time Window 2")
        self.list_time_windows.addItem("Time Window 3")
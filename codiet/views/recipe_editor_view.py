from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QLineEdit,
    QGroupBox,
    QSizePolicy,
    QTextEdit
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

        # Create a 'Basic Info' groupbox
        basic_info_group = QGroupBox("Basic Info")
        column1_layout.addWidget(basic_info_group)
        basic_info_layout = QVBoxLayout()
        basic_info_group.setLayout(basic_info_layout)
        basic_info_layout.setContentsMargins(5, 5, 5, 5)

        # Add a row containg the recipe name label and a textbox
        recipe_name_layout = QHBoxLayout()
        basic_info_layout.addLayout(recipe_name_layout)
        label = QLabel("Name: ")
        recipe_name_layout.addWidget(label)
        self.textbox_recipe_name = QLineEdit()
        recipe_name_layout.addWidget(self.textbox_recipe_name)

        # Add a row containing the recipe instructions label and multiline textbox
        label = QLabel("Instructions:")
        basic_info_layout.addWidget(label)
        self.textbox_recipe_instructions = QTextEdit()
        basic_info_layout.addWidget(self.textbox_recipe_instructions)

        # Create the second column
        column2_layout = QVBoxLayout()
        columns_layout.addLayout(column2_layout, 2)

        # Create the ingredients group within the second col
        ingredients_group = QGroupBox("Ingredients")
        column2_layout.addWidget(ingredients_group)
        ingredients_layout = QVBoxLayout()
        ingredients_group.setLayout(ingredients_layout)
        ingredients_layout.setContentsMargins(5, 5, 5, 5)

        # Create an add ingredient button
        self.btn_add_ingredient = QPushButton("Add Ingredient")
        ingredients_layout.addWidget(self.btn_add_ingredient)

        # Create a list widget to hold the ingredients
        self.list_ingredients = QListWidget()
        ingredients_layout.addWidget(self.list_ingredients)
        # Add some dummy ingredients for now
        self.list_ingredients.addItem("Ingredient 1")
        self.list_ingredients.addItem("Ingredient 2")
        self.list_ingredients.addItem("Ingredient 3")

        # Create the third column
        column3_layout = QVBoxLayout()
        columns_layout.addLayout(column3_layout, 1)

        # Put a group inside the third column called 'Time'
        time_group = QGroupBox("Time")
        column3_layout.addWidget(time_group)
        time_layout = QVBoxLayout()
        time_group.setLayout(time_layout)
        time_layout.setContentsMargins(5, 5, 5, 5)

        # Create a button to add a time window
        self.btn_add_time_window = QPushButton("Add Time Window")
        time_layout.addWidget(self.btn_add_time_window)

        # Create a list widget to hold the time windows
        self.list_time_windows = QListWidget()
        time_layout.addWidget(self.list_time_windows)
        # Add some dummy time windows for now
        self.list_time_windows.addItem("Time Window 1")
        self.list_time_windows.addItem("Time Window 2")
        self.list_time_windows.addItem("Time Window 3")

        # At the bottom of the page, put a 'Save Recipe' button
        self.btn_save_recipe = QPushButton("Save Recipe")
        self.btn_save_recipe.setMaximumWidth(150)
        page_layout.addWidget(self.btn_save_recipe)

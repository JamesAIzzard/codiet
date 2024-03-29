from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QGroupBox,
    QTextEdit,
)
from PyQt6.QtGui import QFont

from codiet.views.ingredients_editor_view import IngredientsEditorView
from codiet.views.serve_time_intervals_editor_view import ServeTimeIntervalsEditorView
from codiet.views.recipe_type_selector_view import RecipeTypeSelectorView

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

        # Add a row containing the recipe description label and multiline textbox
        label = QLabel("Description:")
        basic_info_layout.addWidget(label)
        self.textbox_recipe_description = QTextEdit()
        basic_info_layout.addWidget(self.textbox_recipe_description)
        # Make the description box just three lines high
        self.textbox_recipe_description.setFixedHeight(60)

        # Add a row containing the recipe instructions label and multiline textbox
        label = QLabel("Instructions:")
        basic_info_layout.addWidget(label)
        self.textbox_recipe_instructions = QTextEdit()
        basic_info_layout.addWidget(self.textbox_recipe_instructions)

        # Create the second column
        lyt_col_2 = QVBoxLayout()
        columns_layout.addLayout(lyt_col_2, 2)

        # Add the ingredients editor widget to the second col
        self.ingredients_editor = IngredientsEditorView()
        lyt_col_2.addWidget(self.ingredients_editor)

        # Create the third column
        lyt_col_3 = QVBoxLayout()
        columns_layout.addLayout(lyt_col_3, 1)

        # Add the serve times editor widget to the third col
        self.serve_time_intervals_editor_view = ServeTimeIntervalsEditorView()
        lyt_col_3.addWidget(self.serve_time_intervals_editor_view)

        # Add the recipe type selector widget to the third col
        self.recipe_type_selector_view = RecipeTypeSelectorView()
        lyt_col_3.addWidget(self.recipe_type_selector_view)

        # At the bottom of the page, put a 'Save Recipe' button
        self.btn_save_recipe = QPushButton("Save Recipe")
        self.btn_save_recipe.setMaximumWidth(150)
        page_layout.addWidget(self.btn_save_recipe)

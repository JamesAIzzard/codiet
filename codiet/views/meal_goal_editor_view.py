from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QGroupBox,
    QTextEdit,
    QCheckBox
)
from PyQt6.QtGui import QFont

from codiet.views.nutrient_targets_editor_view import NutrientTargetsEditorView
from codiet.views.flag_editor_view import FlagEditorView
from codiet.views.gi_editor_view import GIEditorView
from codiet.views.recipe_type_selector_view import RecipeTypeSelectorView

class MealGoalEditorView(QWidget):
    """The UI element to allow the user to edit a meal goal."""
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the page
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)

        # Create a label and add it to the layout
        label = QLabel("Meal Goal Editor")
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        lyt_top_level.addWidget(label)

        # Create a horizontal layout for the columns
        lyt_columns = QHBoxLayout()
        lyt_top_level.addLayout(lyt_columns)

        # Create the first column
        lyt_basic_info = QVBoxLayout()
        lyt_columns.addLayout(lyt_basic_info)
        # Set the width ratio of the first column
        lyt_columns.setStretch(0, 2)

        # Create the Basic Info groupbox
        basic_info_group = QGroupBox("Basic Info")
        lyt_basic_info.addWidget(basic_info_group)
        basic_info_layout = QVBoxLayout()
        basic_info_group.setLayout(basic_info_layout)
        basic_info_layout.setContentsMargins(5, 5, 5, 5)

        # Add a row containing the meal name and textbox
        meal_name_layout = QHBoxLayout()
        basic_info_layout.addLayout(meal_name_layout)
        label = QLabel("Meal Type: ")
        meal_name_layout.addWidget(label)
        self.textbox_meal_name = QLineEdit()
        meal_name_layout.addWidget(self.textbox_meal_name)

        # Add a row containing the recipe instructions label and multiline textbox
        label = QLabel("Description:")
        basic_info_layout.addWidget(label)
        self.textbox_meal_description = QTextEdit()
        basic_info_layout.addWidget(self.textbox_meal_description)

        # Add a flag editor view
        self.flag_editor_view = FlagEditorView()
        lyt_basic_info.addWidget(self.flag_editor_view)

        # Add a GI editor view
        self.gi_editor_view = GIEditorView()
        lyt_basic_info.addWidget(self.gi_editor_view)

        # Add the nutrient targets editor to the second column
        self.nutrient_targets_editor_view = NutrientTargetsEditorView()
        lyt_columns.addWidget(self.nutrient_targets_editor_view)
        lyt_columns.setStretch(1, 2)
        
        # Add the recipe types selector UI element
        self.recipe_type_selector_view = RecipeTypeSelectorView()
        lyt_columns.addWidget(self.recipe_type_selector_view)
        lyt_columns.setStretch(2, 1)

        # At the bottom of the page, put a save meal button
        self.btn_save_meal = QPushButton("Save Meal")
        self.btn_save_meal.setMaximumWidth(150)
        lyt_top_level.addWidget(self.btn_save_meal)
        

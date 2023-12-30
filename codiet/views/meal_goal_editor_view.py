from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QLineEdit,
    QGroupBox,
    QTextEdit,
    QComboBox
)
from PyQt6.QtGui import QFont

from codiet.views.nutrient_targets_editor_view import NutrientTargetsEditorView

class MealGoalEditorView(QWidget):
    """The UI element to allow the user to edit a meal goal."""
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the page
        page_layout = QVBoxLayout()
        self.setLayout(page_layout)

        # Create a label and add it to the layout
        label = QLabel("Meal Editor")
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        page_layout.addWidget(label)

        # Create a horizontal layout for the columns
        columns_layout = QHBoxLayout()
        page_layout.addLayout(columns_layout)

        # Create the first column
        column1_layout = QVBoxLayout()
        columns_layout.addLayout(column1_layout)

        # Create the Basic Info groupbox
        basic_info_group = QGroupBox("Basic Info")
        column1_layout.addWidget(basic_info_group)
        basic_info_layout = QVBoxLayout()
        basic_info_group.setLayout(basic_info_layout)
        basic_info_layout.setContentsMargins(5, 5, 5, 5)

        # Add a row containing the meal name and textbox
        meal_name_layout = QHBoxLayout()
        basic_info_layout.addLayout(meal_name_layout)
        label = QLabel("Name: ")
        meal_name_layout.addWidget(label)
        self.textbox_meal_name = QLineEdit()
        meal_name_layout.addWidget(self.textbox_meal_name)

        # Add a row containing the recipe instructions label and multiline textbox
        label = QLabel("Description:")
        basic_info_layout.addWidget(label)
        self.textbox_meal_description = QTextEdit()
        basic_info_layout.addWidget(self.textbox_meal_description)

        # Add a row containing the meal time and textbox
        meal_time_layout = QHBoxLayout()
        basic_info_layout.addLayout(meal_time_layout)
        label = QLabel("Meal Time: ")
        meal_time_layout.addWidget(label)
        self.textbox_meal_time = QLineEdit()
        meal_time_layout.addWidget(self.textbox_meal_time)

        # Add a row containing the meal target cost
        meal_cost_layout = QHBoxLayout()
        basic_info_layout.addLayout(meal_cost_layout)
        label = QLabel("Max Cost: £")
        meal_cost_layout.addWidget(label)
        self.textbox_meal_cost = QLineEdit()
        meal_cost_layout.addWidget(self.textbox_meal_cost)

        # Add a row containing a label and a combo box for the meal class
        meal_class_layout = QHBoxLayout()
        basic_info_layout.addLayout(meal_class_layout)
        label = QLabel("Meal Class: ")
        meal_class_layout.addWidget(label)
        self.dropdown_meal_class = QComboBox()
        # Generate some dummy meal classes
        self.dropdown_meal_class.addItem("Breakfast")
        self.dropdown_meal_class.addItem("Lunch")
        self.dropdown_meal_class.addItem("Dinner")
        self.dropdown_meal_class.addItem("Snack")
        self.dropdown_meal_class.addItem("Dessert")
        self.dropdown_meal_class.addItem("Drink")
        meal_class_layout.addWidget(self.dropdown_meal_class)

        # Create a second column
        column2_layout = QVBoxLayout()
        columns_layout.addLayout(column2_layout)

        # Put a nutrient targets editor view in it
        self.nutrient_targets_editor_view = NutrientTargetsEditorView()
        column2_layout.addWidget(self.nutrient_targets_editor_view)

        # At the bottom of the page, put a save meal button
        self.btn_save_meal = QPushButton("Save Meal")
        self.btn_save_meal.setMaximumWidth(150)
        page_layout.addWidget(self.btn_save_meal)
        
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
    QListWidgetItem,
)
from PyQt6.QtGui import QFont

from codiet.views.day_plan_meal_view import DayPlanMealView

class DayPlanEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a top level layout for the page
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)

        # Create a label and add it to the layout
        label = QLabel("Day Plan Editor")
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        lyt_top_level.addWidget(label)

        # Add a horizontal layout to the top level layout
        # to split the page into two cols
        lyt_split_page = QHBoxLayout()
        lyt_top_level.addLayout(lyt_split_page)

        # In the first col, put a vertical layout
        lyt_first_col = QVBoxLayout()
        lyt_split_page.addLayout(lyt_first_col, 2)

        # In the first col, add the day name textbox and label
        lyt_day_name = QHBoxLayout()
        lyt_first_col.addLayout(lyt_day_name)
        lbl_name = QLabel("Day Plan Name: ")
        lyt_day_name.addWidget(lbl_name)
        self.txt_name = QLineEdit()
        lyt_day_name.addWidget(self.txt_name)

        # In the first col add a horizontal layout for buttons
        lyt_buttons = QHBoxLayout()
        lyt_first_col.addLayout(lyt_buttons)
        # Add an 'Add Meal' button to the first col
        btn_add_meal = QPushButton("Add")
        lyt_buttons.addWidget(btn_add_meal)
        # Add a 'Remove Meal' button to the first col
        btn_remove_meal = QPushButton("Remove")
        lyt_buttons.addWidget(btn_remove_meal)
        # Add a 'Reorder Meals' button to the first col
        btn_reorder_meals = QPushButton("Reorder")
        lyt_buttons.addWidget(btn_reorder_meals)

        # Now add the listbox for the meals
        # Each meal is a DayPlanMealView
        self.lst_meals = QListWidget()
        lyt_first_col.addWidget(self.lst_meals)
        # Add a couple of meals to the listbox
        self.add_meal_view("Breakfast")
        self.add_meal_view("Pre Run Snack")
        self.add_meal_view("Lunch")
        self.add_meal_view("Dinner")

        # Add the second col to the page
        lyt_second_col = QVBoxLayout()
        lyt_split_page.addLayout(lyt_second_col, 1)

        # In the second col of top level add the summary groupbox
        gb_summary = QGroupBox("Summary")
        lyt_second_col.addWidget(gb_summary)

        # Add a vertical layout to the groupbox to contain basic info rows
        lyt_summary = QVBoxLayout()
        gb_summary.setLayout(lyt_summary)
        lyt_summary.setContentsMargins(5, 5, 5, 5)

        # Add a row containing the calorie summary
        lyt_calorie_summary = QHBoxLayout()
        lyt_summary.addLayout(lyt_calorie_summary)
        lbl_calories = QLabel("Total Calories: ...")
        lyt_calorie_summary.addWidget(lbl_calories)
        # Add a 'Set' button
        btn_set_calories = QPushButton("Set")
        btn_set_calories.setMaximumWidth(40)
        lyt_calorie_summary.addWidget(btn_set_calories)

        # Add a row containing the cost summary
        lyt_cost_summary = QHBoxLayout()
        lyt_summary.addLayout(lyt_cost_summary)
        lbl_cost = QLabel("Total Cost: £...")
        lyt_cost_summary.addWidget(lbl_cost)
        # Add a 'Set' button
        btn_set_cost = QPushButton("Set")
        btn_set_cost.setMaximumWidth(40)
        lyt_cost_summary.addWidget(btn_set_cost)

        # Push items to top
        lyt_summary.addStretch(1)

        # Add a save day button to the bottom of the page
        btn_save_day_plan = QPushButton("Save Day Plan")
        lyt_top_level.addWidget(btn_save_day_plan)
        # Make text width set the width of the button
        btn_save_day_plan.setMaximumWidth(150)

    def add_meal_view(self, meal_name: str):
        meal = DayPlanMealView()
        # meal.txt_meal_name.setText(meal_name)
        item = QListWidgetItem(self.lst_meals)
        # Make sure the widget is large enough to show
        # the custom contents
        item.setSizeHint(meal.sizeHint())
        # Add the item to the list
        self.lst_meals.addItem(item)
        # Set the widget for the item
        self.lst_meals.setItemWidget(item, meal)


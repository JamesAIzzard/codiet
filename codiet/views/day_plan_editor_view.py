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

        # As the first row of the overall vertical layout
        # create a horizontal layout.
        lyt_first_row = QHBoxLayout()
        # Add the first row to the top level layout
        lyt_top_level.addLayout(lyt_first_row)

        # The first column of this hz layout will contain the basic
        # info groupbox.
        gb_basic_info = QGroupBox("Basic Info")
        lyt_first_row.addWidget(gb_basic_info)

        # Add a vertical layout to the groupbox to contain basic info rows
        lyt_basic_info = QVBoxLayout()
        gb_basic_info.setLayout(lyt_basic_info)
        lyt_basic_info.setContentsMargins(5, 5, 5, 5)

        # Add a row containing the day plan name label and a textbox
        lyt_day_name = QHBoxLayout()
        lyt_basic_info.addLayout(lyt_day_name)
        lbl_name = QLabel("Name: ")
        lyt_day_name.addWidget(lbl_name)
        self.txt_name = QLineEdit()
        lyt_day_name.addWidget(self.txt_name)

        # Add a row containing the calorie summary
        lyt_calorie_summary = QHBoxLayout()
        lyt_basic_info.addLayout(lyt_calorie_summary)
        lbl_calories = QLabel("Total Calories: ...")
        lyt_calorie_summary.addWidget(lbl_calories)

        # Add a row containing the cost summary
        lyt_cost_summary = QHBoxLayout()
        lyt_basic_info.addLayout(lyt_cost_summary)
        lbl_cost = QLabel("Total Cost: £...")
        lyt_cost_summary.addWidget(lbl_cost)

        # To the second column, add the Add Meal button
        btn_add_meal = QPushButton("Add Meal")
        lyt_first_row.addWidget(btn_add_meal)

        # Make the two columns in the first row take up equal space
        lyt_first_row.setStretch(0, 1)
        lyt_first_row.setStretch(1, 1)

        # Add a listbox to the page to contain the meals.
        # Each meal is a DayPlanMealView
        self.lst_meals = QListWidget()
        lyt_top_level.addWidget(self.lst_meals)
        # Add a couple of meals to the listbox
        meal1 = DayPlanMealView()
        self.add_meal_view("Breakfast")
        self.add_meal_view("Lunch")

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


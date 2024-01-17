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

from day_plan_meal_view import DayPlanMealView

class DayPlanEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a top level layout for the page
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)
        # Add a groupbox to contain day plan 'Basic Info'
        gb_basic_info = QGroupBox("Basic Info")
        lyt_top_level.addWidget(gb_basic_info)

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
        # Add a row containing the max day cost
        lyt_max_day_cost = QHBoxLayout()
        lyt_basic_info.addLayout(lyt_max_day_cost)
        lbl_max_day_cost = QLabel("Max Day Cost: £")
        lyt_max_day_cost.addWidget(lbl_max_day_cost)
        self.txt_max_day_cost = QLineEdit()
        lyt_max_day_cost.addWidget(self.txt_max_day_cost)

        # Add a horizontal layout to the groupbox to contain calorie summary
        # and Add Meal button.
        lyt_utils = QHBoxLayout()
        lyt_basic_info.addLayout(lyt_utils)
        # To the first column, add the total calories summary
        lbl_calories = QLabel("Total Calories: ...")
        lyt_utils.addWidget(lbl_calories)
        # To the second column, add the Add Meal button
        btn_add_meal = QPushButton("Add Meal")
        lyt_utils.addWidget(btn_add_meal)

        # Add a listbox to the page to contain the meals.
        # Each meal is a DayPlanMealView
        self.lst_meals = QListWidget()
        lyt_top_level.addWidget(self.lst_meals)
        # Add a couple of meals to the listbox
        meal1 = DayPlanMealView()
        meal1.txt_meal_name.setText("Meal 1")
        meal2 = DayPlanMealView()
        meal2.txt_meal_name.setText("Meal 2")
        item1 = QListWidgetItem(self.lst_meals)
        self.lst_meals.setItemWidget(item1, meal1)
        item2 = QListWidgetItem(self.lst_meals)
        self.lst_meals.setItemWidget(item2, meal2)


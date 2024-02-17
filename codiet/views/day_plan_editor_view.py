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

from codiet.views.day_plan_meal_view import DayPlanMealView

class DayPlanEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a top level layout for the page
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)

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

        # Add a row containing the max day cost
        lyt_max_day_cost = QHBoxLayout()
        lyt_basic_info.addLayout(lyt_max_day_cost)
        lbl_max_day_cost = QLabel("Max Day Cost: £")
        lyt_max_day_cost.addWidget(lbl_max_day_cost)
        self.txt_max_day_cost = QLineEdit()
        lyt_max_day_cost.addWidget(self.txt_max_day_cost)

        # Add a row containing the calorie summary
        lyt_calorie_summary = QHBoxLayout()
        lyt_basic_info.addLayout(lyt_calorie_summary)
        lbl_calories = QLabel("Total Calories: ...")
        lyt_calorie_summary.addWidget(lbl_calories)

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

    def add_meal_view(self, meal_name: str):
        meal = DayPlanMealView()
        meal.txt_meal_name.setText(meal_name)
        item = QListWidgetItem(self.lst_meals)
        # Make sure the widget is large enough to show
        # the custom contents
        item.setSizeHint(meal.sizeHint())
        # Add the item to the list
        self.lst_meals.addItem(item)
        # Set the widget for the item
        self.lst_meals.setItemWidget(item, meal)


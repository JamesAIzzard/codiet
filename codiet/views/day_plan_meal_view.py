from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QSizePolicy,
)

class DayPlanMealView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a top level layout
        lyt_top_level = QHBoxLayout()
        self.setLayout(lyt_top_level)

        # Create the first row and add two rows
        lyt_first_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_first_col, 1)
        # In the first row, create a label and a textbox
        lyt_meal_name = QHBoxLayout()
        label = QLabel("Meal Name:")
        lyt_meal_name.addWidget(label)
        self.txt_meal_name = QLineEdit()
        lyt_meal_name.addWidget(self.txt_meal_name)
        lyt_first_col.addLayout(lyt_meal_name)

        # Add the meal time stuff to the second row
        lyt_meal_time = QHBoxLayout()
        label = QLabel("Meal Time:")
        lyt_meal_time.addWidget(label)
        self.txt_meal_description = QLineEdit()
        lyt_meal_time.addWidget(self.txt_meal_description)
        lyt_first_col.addLayout(lyt_meal_time)

        # Create the second column and add two rows
        lyt_second_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_second_col, 1)
        # In the first row, create a dropdown list
        self.drp_meal_goal = QComboBox()
        # Add some dummy meal goal names
        self.drp_meal_goal.addItem("Pre-Run Breakfast")
        self.drp_meal_goal.addItem("Post-Run Breakfast")
        self.drp_meal_goal.addItem("Lunch")
        # Add the dropdown to the layout
        lyt_second_col.addWidget(self.drp_meal_goal)

        # In the second row, create a label and textbox in a horizontal layout
        lyt_calories = QHBoxLayout()
        label = QLabel("Calories:")
        lyt_calories.addWidget(label)
        self.txt_calories = QLineEdit()
        lyt_calories.addWidget(self.txt_calories)
        lyt_second_col.addLayout(lyt_calories)

        # In the third column, create a remove button
        btn_remove = QPushButton("X")
        btn_remove.setMaximumWidth(30)
        btn_remove.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        lyt_top_level.addWidget(btn_remove)



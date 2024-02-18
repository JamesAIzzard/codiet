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

        # Create 4 columns in the widget
        lyt_first_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_first_col, 1)
        lyt_second_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_second_col, 1)
        lyt_third_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_third_col, 1)
        lyt_fourth_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_fourth_col, 1)

        # Add the meal name editor to the first col
        lyt_meal_name = QHBoxLayout()
        label = QLabel("Meal Name:")
        lyt_meal_name.addWidget(label)
        self.txt_meal_name = QLineEdit()
        lyt_meal_name.addWidget(self.txt_meal_name)
        lyt_first_col.addLayout(lyt_meal_name)

        # Add the meal time editor to the first col
        lyt_meal_time = QHBoxLayout()
        label = QLabel("Meal Time:")
        lyt_meal_time.addWidget(label)
        self.txt_meal_description = QLineEdit()
        lyt_meal_time.addWidget(self.txt_meal_description)
        lyt_first_col.addLayout(lyt_meal_time)

        # Add the meal goal dropdown to the second col
        self.drp_meal_goal = QComboBox()
        # Add some dummy meal goal names
        self.drp_meal_goal.addItem("Pre-Run Breakfast")
        self.drp_meal_goal.addItem("Post-Run Breakfast")
        self.drp_meal_goal.addItem("Lunch")
        # Add the dropdown to the layout
        lyt_second_col.addWidget(self.drp_meal_goal)

        # Add the calories editor the the second col
        lyt_calories = QHBoxLayout()
        label = QLabel("Calories:")
        lyt_calories.addWidget(label)
        self.txt_calories = QLineEdit()
        lyt_calories.addWidget(self.txt_calories)
        lyt_second_col.addLayout(lyt_calories)

        # Add a max cost editor to the third col
        lyt_cost = QHBoxLayout()
        label = QLabel("Max Cost:")
        lyt_cost.addWidget(label)
        self.txt_cost = QLineEdit()
        lyt_cost.addWidget(self.txt_cost)
        lyt_third_col.addLayout(lyt_cost)
        # Push to the top of the col
        lyt_third_col.addStretch(1)

        # Add the remove button to the fourth col
        btn_remove = QPushButton("X")
        btn_remove.setMaximumWidth(30)
        btn_remove.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        lyt_fourth_col.addWidget(btn_remove)



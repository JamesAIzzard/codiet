from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QSizePolicy,
    QTimeEdit,
    QFrame,
)

class DayPlanMealView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a top level layout
        lyt_top_level = QHBoxLayout()
        self.setLayout(lyt_top_level)
        # Control padding
        lyt_top_level.setContentsMargins(5, 5, 5, 5)

        # Add the first time column
        lyt_time_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_time_col, 1)

        # The first column is to set the mealtime
        # Add a 'Mealtime' label to the first col
        label = QLabel("Meal Time")
        lyt_time_col.addWidget(label)
        # Add a time editor to the first col
        self.txt_meal_time = QTimeEdit()
        lyt_time_col.addWidget(self.txt_meal_time)
        # Set the max width of the time editor
        self.txt_meal_time.setMaximumWidth(55)

        # Add a seperator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet("background-color: gray;") 
        lyt_top_level.addWidget(separator)

        # Add the name and type column
        lyt_name_and_type_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_name_and_type_col, 1)

        # Add the meal name editor to the name and type col
        lyt_meal_name = QHBoxLayout()
        lyt_name_and_type_col.addLayout(lyt_meal_name)
        # Var to hold text field widths of this col
        text_width = 220
        label = QLabel("Meal Name:")
        lyt_meal_name.addWidget(label)
        self.txt_meal_name = QLineEdit()
        # Set the max width of the meal name editor
        self.txt_meal_name.setMaximumWidth(text_width)
        lyt_meal_name.addWidget(self.txt_meal_name)

        # Add the meal type dropdown to the name and type col
        lyt_meal_type = QHBoxLayout()
        lyt_name_and_type_col.addLayout(lyt_meal_type)
        label = QLabel("Meal Type:")
        lyt_meal_type.addWidget(label)
        # Add the meal goal dropdown to the second col
        self.drp_meal_goal = QComboBox()
        # Set the width of the meal goal dropdown
        self.drp_meal_goal.setMaximumWidth(text_width)
        self.drp_meal_goal.setMinimumWidth(text_width)
        # Add some dummy meal goal names
        self.drp_meal_goal.addItem("Pre-Run Breakfast")
        self.drp_meal_goal.addItem("Post-Run Breakfast")
        self.drp_meal_goal.addItem("Lunch")
        # Add the dropdown to the layout
        lyt_meal_type.addWidget(self.drp_meal_goal)

        # Add the calories and cost col
        lyt_calories_and_cost = QVBoxLayout()
        lyt_top_level.addLayout(lyt_calories_and_cost, 0)
        # Add the calories editor the the second col
        lyt_calories = QHBoxLayout()
        lyt_calories_and_cost.addLayout(lyt_calories)
        label = QLabel("Calories:")
        lyt_calories.addWidget(label)
        self.txt_calories = QLineEdit()
        lyt_calories.addWidget(self.txt_calories)
        lyt_calories.addWidget(QLabel("kcal"))

        # Add a max cost editor to the third col
        lyt_cost = QHBoxLayout()
        lyt_calories_and_cost.addLayout(lyt_cost)
        label = QLabel("Max Cost: £")
        lyt_cost.addWidget(label)
        self.txt_cost = QLineEdit()
        lyt_cost.addWidget(self.txt_cost)

        # Add a spacer to push the meal view to the left
        lyt_top_level.addStretch(1)



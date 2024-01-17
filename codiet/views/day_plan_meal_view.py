from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QLineEdit,
    QTextEdit,
)

class DayPlanMealView(QWidget):
    def __init__(self):
        super().__init__()

        # Create three vertical columns
        lyt_top_level = QHBoxLayout()
        self.setLayout(lyt_top_level)

        # Create the first column and add two rows
        lyt_first_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_first_col, 1)
        # In the first row, create a label and a textbox
        label = QLabel("Meal Name:")
        lyt_first_col.addWidget(label)
        self.txt_meal_name = QLineEdit()
        lyt_first_col.addWidget(self.txt_meal_name)
        # In the second row create a label and a textbox
        label = QLabel("Meal Time:")
        lyt_first_col.addWidget(label)
        self.txt_meal_description = QTextEdit()
        lyt_first_col.addWidget(self.txt_meal_description)

        # Create the second column and add two rows
        lyt_second_col = QVBoxLayout()
        lyt_top_level.addLayout(lyt_second_col, 1)
        # In the first row, create a dropdown list
        self.drp_meal_goal = QListWidget()
        # In the second row, create a label and textbox
        label = QLabel("Calories:")
        lyt_second_col.addWidget(label)
        self.txt_calories = QLineEdit()
        lyt_second_col.addWidget(self.txt_calories)

        # In the third column, create a remove button
        btn_remove = QPushButton("X")
        btn_remove.setMaximumWidth(30)
        lyt_top_level.addWidget(btn_remove)



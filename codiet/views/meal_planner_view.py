from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from PyQt6.QtGui import QFont

from codiet.views.buttons import AddButton, RemoveButton, SolveButton

class MealPlannerView(QWidget):
    """UI element to allow the user to plan meals."""
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        """Build the UI elements."""
        # Create a vertical layout to hold the title at the top, and
        # the columns layout underneath
        lyt_top_level = QVBoxLayout()
        # Set the layout for the page
        self.setLayout(lyt_top_level)

        # Create the page title
        lbl_title = QLabel("Meal Planner")
        lbl_title.setProperty("class", "page-title")
        lyt_top_level.addWidget(lbl_title)

        # Create a horizontal layout for the page columns
        lyt_columns = QHBoxLayout()
        lyt_top_level.addLayout(lyt_columns)

        # Add the days column to the columns layout
        lyt_days_column = QVBoxLayout()
        lyt_columns.addLayout(lyt_days_column)
        # Add a horizontal layout to hold the label and buttons for the days column
        lyt_days_top_row = QHBoxLayout()
        # Add a label for the days column
        lbl_days = QLabel("Days:")
        lyt_days_top_row.addWidget(lbl_days)
        # Add buttons to add and remove days
        btn_add_day = AddButton()
        lyt_days_top_row.addWidget(btn_add_day)
        btn_remove_day = RemoveButton()
        lyt_days_top_row.addWidget(btn_remove_day)
        # Add a solve button
        btn_solve = SolveButton()
        lyt_days_top_row.addWidget(btn_solve)

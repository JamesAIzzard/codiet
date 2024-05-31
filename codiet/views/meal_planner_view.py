from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget
)

from codiet.views.buttons import AddButton, RemoveButton, SolveButton
from codiet.views.search import SearchTermView

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
        # Build the days column UI
        self._build_days_col_ui(lyt_days_column)

        # Add the meals column to the columns layout
        lyt_meals_column = QVBoxLayout()
        lyt_columns.addLayout(lyt_meals_column)
        # Build the meals column UI
        self._build_meals_col_ui(lyt_meals_column)

        # Add the goals column to the columns layout
        lyt_goals_column = QVBoxLayout()
        lyt_columns.addLayout(lyt_goals_column)
        # Build the goals column UI
        self._build_goals_col_ui(lyt_goals_column)

        # Add the constraints column to the columns layout
        lyt_constraints_column = QVBoxLayout()
        lyt_columns.addLayout(lyt_constraints_column)
        # Build the constraints column UI
        self._build_constraints_col_ui(lyt_constraints_column)

        # Stretch factor for each column within the horizontal layout for even distribution
        lyt_columns.setStretch(0, 1)  # days column
        lyt_columns.setStretch(1, 1)  # meals column
        lyt_columns.setStretch(2, 1)  # goals column
        lyt_columns.setStretch(3, 1)  # constraints column

    def _build_days_col_ui(self, lyt_days_column):
        """Populate the column layout with the days UI elements."""
        # Add a horizontal layout to hold the label and buttons for the days column
        lyt_days_top_row = QHBoxLayout()
        lyt_days_column.addLayout(lyt_days_top_row)
        # Add a label for the days column
        lbl_days = QLabel("Days:")
        lyt_days_top_row.addWidget(lbl_days)
        # Add buttons to add and remove days
        btn_add_day = AddButton()
        lyt_days_top_row.addWidget(btn_add_day)
        btn_remove_day = RemoveButton()
        lyt_days_top_row.addWidget(btn_remove_day)
        # Add a solve button
        btn_solve_day = SolveButton()
        lyt_days_top_row.addWidget(btn_solve_day)
        # Push buttons to RHS
        lyt_days_top_row.addStretch()
        
        # Add a search view
        self.days_search_view = SearchTermView()
        lyt_days_column.addWidget(self.days_search_view)
        
        # Add a list widget to hold the days
        self.lst_days = QListWidget() 
        lyt_days_column.addWidget(self.lst_days)

    def _build_meals_col_ui(self, lyt_meals_column):
        """Populate the column layout with the meals UI elements."""
        # Add a horizontal layout to hold the label and buttons for the meals column
        lyt_meals_top_row = QHBoxLayout()
        lyt_meals_column.addLayout(lyt_meals_top_row)
        # Add a label for the meals column
        lbl_meals = QLabel("Meals:")
        lyt_meals_top_row.addWidget(lbl_meals)
        # Add buttons to add and remove meals
        btn_add_meal = AddButton()
        lyt_meals_top_row.addWidget(btn_add_meal)
        btn_remove_meal = RemoveButton()
        lyt_meals_top_row.addWidget(btn_remove_meal)
        # Add a solve button
        btn_solve_meal = SolveButton()
        lyt_meals_top_row.addWidget(btn_solve_meal)
        # Push buttons to RHS
        lyt_meals_top_row.addStretch()
        
        # Add a search view
        self.meals_search_view = SearchTermView()
        lyt_meals_column.addWidget(self.meals_search_view)
        
        # Add a list widget to hold the meals
        self.lst_meals = QListWidget() 
        lyt_meals_column.addWidget(self.lst_meals)

    def _build_goals_col_ui(self, lyt_goals_column):
        """Populate the column layout with the goals UI elements."""
        # Add a horizontal layout ot hold the label and buttons for the goals column
        lyt_goals_top_row = QHBoxLayout()
        lyt_goals_column.addLayout(lyt_goals_top_row)
        # Add a label for the goals column
        lbl_goals = QLabel("Goals:")
        lyt_goals_top_row.addWidget(lbl_goals)
        # Add buttons to add and remove goals
        btn_add_goal = AddButton()
        lyt_goals_top_row.addWidget(btn_add_goal)
        btn_remove_goal = RemoveButton()
        lyt_goals_top_row.addWidget(btn_remove_goal)
        # Push buttons to the RHS
        lyt_goals_top_row.addStretch()

        # Add a search view
        self.goals_search_view = SearchTermView()
        lyt_goals_column.addWidget(self.goals_search_view)

        # Add a list widget to hold the goals
        self.lst_goals = QListWidget()
        lyt_goals_column.addWidget(self.lst_goals)

    def _build_constraints_col_ui(self, lyt_constraints_column):
        """Populate the column layout with the constraints UI elements."""
        # Add a horizontal layout to hold the label and buttons for the constraints column
        lyt_constraints_top_row = QHBoxLayout()
        lyt_constraints_column.addLayout(lyt_constraints_top_row)
        # Add a label for the constraints column
        lbl_constraints = QLabel("Constraints:")
        lyt_constraints_top_row.addWidget(lbl_constraints)
        # Add buttons to add and remove constraints
        btn_add_constraint = AddButton()
        lyt_constraints_top_row.addWidget(btn_add_constraint)
        btn_remove_constraint = RemoveButton()
        lyt_constraints_top_row.addWidget(btn_remove_constraint)
        # Push buttons to the RHS
        lyt_constraints_top_row.addStretch()
        
        # Add a search view
        self.constraints_search_view = SearchTermView()
        lyt_constraints_column.addWidget(self.constraints_search_view)

        # Add a list widget to hold the constraints
        self.lst_constraints = QListWidget()
        lyt_constraints_column.addWidget(self.lst_constraints)
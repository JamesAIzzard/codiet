from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QToolBar,
    QStatusBar,
)
from PyQt6.QtCore import pyqtSignal

from codiet.views import load_icon
from codiet.views.buttons import IconButton

class MainWindowView(QMainWindow):
    """The main window view for the CoDiet application."""
    # Define signals
    ingredientsClicked = pyqtSignal()
    recipesClicked = pyqtSignal()
    mealPlannerClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("CoDiet - Computational Nutrition")
        # Set the window size
        self.resize(1400, 900)
        # Set the window icon
        self.setWindowIcon(load_icon("app-icon.png"))

        # Build the UI
        self._build_ui()

        # Create a dict for the individual pages
        self._pages = {}

    def add_page(self, name: str, page):
        """Adds a page to the stacked widget."""
        self._pages[name] = page
        self._page_stack.addWidget(page)

    def show_page(self, name: str):
        """Shows the page with the given name."""
        self._page_stack.setCurrentWidget(self._pages[name])

    def deselect_all_nav_buttons(self):
        """Deselects all navigation buttons."""
        self.btn_ingredients.deselect()
        self.btn_recipes.deselect()
        self.btn_meal_planner.deselect()

    def _build_ui(self) -> None:
        """Builds the main page UI."""
        # Add a toolbar
        self._build_toolbar()
        # Create a stacked widget to hold the pages
        self._page_stack = QStackedWidget()
        self.setCentralWidget(self._page_stack)

        # Add a footer bar
        self._build_footer()

    def _build_toolbar(self) -> None:
        """Builds the main page menu bar."""
        # Build the toolbar
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)
        # Add an ingredients button
        self.btn_ingredients = IconButton("ingredients-icon.png", "Ingredients")
        self.btn_ingredients.clicked.connect(self.ingredientsClicked.emit)
        toolbar.addWidget(self.btn_ingredients)
        # Add a recipes button
        self.btn_recipes = IconButton("recipes-icon.png", "Recipes")
        self.btn_recipes.clicked.connect(self.recipesClicked.emit)
        toolbar.addWidget(self.btn_recipes)
        # Add a meal planner button
        self.btn_meal_planner = IconButton("meal-planner-icon.png", "Meal Planner")
        self.btn_meal_planner.clicked.connect(self.mealPlannerClicked.emit)
        toolbar.addWidget(self.btn_meal_planner)

    def _build_footer(self) -> None:
        """Builds the footer bar."""
        # Create a status bar
        self.footer = QStatusBar(self)
        # Put a label in the status bar
        self.footer.showMessage("V0.01")
        # Set the status bar for the main window
        self.setStatusBar(self.footer)


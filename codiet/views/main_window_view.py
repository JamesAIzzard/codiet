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
        self.pages = {}

    def add_page(self, name: str, page):
        """Adds a page to the stacked widget."""
        self.pages[name] = page
        self._page_stack.addWidget(page)

    def show_page(self, name: str):
        """Shows the page with the given name."""
        self._page_stack.setCurrentWidget(self.pages[name])

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
        btn_ingredients = IconButton("ingredients-icon.png", "Ingredients")
        btn_ingredients.clicked.connect(self.ingredientsClicked.emit)
        toolbar.addWidget(btn_ingredients)
        # Add a recipes button
        btn_recipes = IconButton("recipes-icon.png", "Recipes")
        btn_recipes.clicked.connect(self.recipesClicked.emit)
        toolbar.addWidget(btn_recipes)
        # Add a meal planner button
        btn_meal_planner = IconButton("meal-planner-icon.png", "Meal Planner")
        btn_meal_planner.clicked.connect(self.mealPlannerClicked.emit)
        toolbar.addWidget(btn_meal_planner)

    def _build_footer(self) -> None:
        """Builds the footer bar."""
        # Create a status bar
        self.footer = QStatusBar(self)
        # Set the status bar for the main window
        self.setStatusBar(self.footer)

